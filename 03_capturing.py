#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ────── imports ────────────────────────────────────────────────────────────────
import os
import time
import json
import shutil
import threading
from datetime import datetime, timedelta
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from utils.Lights import *                 # LepiLED_start(), LepiLED_ende(), …
from utils.Camera import snap_image
from utils.sensor_data import read_sensor_data
from utils.times import Zeit_aktualisieren, get_experiment_times, get_sun
from utils.json_read_write import (
    get_value_from_section,
    write_json,
    read_json,
)
from utils.service import get_disk_space
from utils.log import log_schreiben
from utils.csv_handler import erstelle_und_aktualisiere_csv
from utils.lora import send_lora
from utils.error_handling import error_message
from utils.checksum import checksum        # assumes this helper exists

stop_event = threading.Event()      # shared shutdown flag


# ────── paths / constants ─────────────────────────────────────────────────────
CONFIG_PATH = "./config/Lepmon_config.json"
LOG_PATH    = CONFIG_PATH
API_PORT    = 8000

# ────── globals (shared with API)──────────────────────────────────────────────
current_params_lock  = threading.Lock()
current_params_cache = read_json(CONFIG_PATH)

current_sensor_lock  = threading.Lock()
current_sensor_data: Dict = {}

# ────── helpers ───────────────────────────────────────────────────────────────
def update_params_cache() -> None:
    with current_params_lock:
        current_params_cache.clear()
        current_params_cache.update(read_json(CONFIG_PATH))

def save_params(data: Dict) -> None:
    write_json(CONFIG_PATH, data)
    update_params_cache()

def set_gps(lat: float, lon: float) -> None:
    with current_params_lock:
        cfg = current_params_cache.copy()
        cfg.setdefault("gps", {})["lat"]  = lat
        cfg["gps"]["lon"]                = lon
        save_params(cfg)

def append_log(msg: str) -> None:
    log_schreiben(msg, LOG_PATH)

# wrappers in case utils.Lights doesn’t expose visible‑LED helpers
try:
    VisibleLED_start
except NameError:
    def VisibleLED_start(): LED_on()
    def VisibleLED_ende():  LED_off()

# ────── FastAPI definition ────────────────────────────────────────────────────
app = FastAPI(title="LepmonOS API")

class GPSCoords(BaseModel):
    lat: float
    lon: float

@app.get("/params")
def api_get_params():
    with current_params_lock:
        return current_params_cache

@app.post("/uv_led/{action}")
def api_uv_led(action: str):
    if action == "on":
        LepiLED_start()
    elif action == "off":
        LepiLED_ende()
    else:
        raise HTTPException(400, "action must be 'on' or 'off'")
    append_log(f"UV LED {action}")
    return {"uv_led": action}

@app.post("/led/{action}")
def api_visible_led(action: str):
    if action == "on":
        VisibleLED_start()
    elif action == "off":
        VisibleLED_ende()
    else:
        raise HTTPException(400, "action must be 'on' or 'off'")
    append_log(f"LED {action}")
    return {"led": action}

@app.post("/gps")
def api_set_gps(coords: GPSCoords):
    set_gps(coords.lat, coords.lon)
    append_log(f"GPS updated to {coords.lat}, {coords.lon}")
    return {"gps": coords}

@app.get("/sensors")
def api_get_sensors():
    with current_sensor_lock:
        return current_sensor_data

@app.get("/log")
def api_get_log(lines: int = 200):
    try:
        with open(LOG_PATH) as f:
            return {"log": f.readlines()[-lines:]}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/shutdown")
def api_shutdown():
    """gracefully stop acquisition loop *and* API server"""
    stop_event.set()
    return {"detail": "shutdown initiated"}

def run_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=API_PORT, log_level="info")
    server = uvicorn.Server(config)

    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    stop_event.wait()          # block here until shutdown is requested
    server.should_exit = True  # signal uvicorn to stop
    server_thread.join()
    
def main_loop():
    
    try:
        total_space_gb, used_space_gb, free_space_gb, used_percent, free_percent = get_disk_space()
        append_log(f"USB Speicher gesamt: {total_space_gb} GB")
        append_log(f"USB Speicher belegt: {used_space_gb} GB  {used_percent} %")
        append_log(f"USB Speicher frei:   {free_space_gb} GB  {free_percent} %")
    except Exception as e:
        error_message(3, e)

    experiment_start_time, experiment_end_time, LepiLed_end_time, _, _ = get_experiment_times()
    _, sunrise, _ = get_sun()
    sunrise = sunrise.strftime('%H:%M:%S')

    try:
        dusk_treshold   = get_value_from_section(CONFIG_PATH, "capture_mode", "dusk_treshold")
        interval        = get_value_from_section(CONFIG_PATH, "capture_mode", "interval")
        initial_exposure= get_value_from_section(CONFIG_PATH, "capture_mode", "initial_exposure")
    except Exception as e:
        error_message(11, e)

    Fang_begonnen      = False
    UV_active          = False
    Kamera_Fehlerserie = 0

    append_log("Beginne Daten und Bildaufnahme")

    try:
        ordner      = get_value_from_section(CONFIG_PATH, "general", "current_folder")
        Dateiname   = os.path.basename(ordner)
        zieldatei   = os.path.join(ordner, f"{Dateiname}_Kameraeinstellungen.xml")
        shutil.copy("/home/pi/LepmonOS/Kamera_Einstellungen.xml", zieldatei)
        checksum(zieldatei, algorithm="md5")
    except Exception:
        pass

    while not stop_event.is_set():
        _, lokale_Zeit = Zeit_aktualisieren()
        sensors        = read_sensor_data("check Lux", lokale_Zeit)
        ambient_light  = sensors["LUX"]

        if (ambient_light <= dusk_treshold and not experiment_end_time <= lokale_Zeit <= experiment_start_time) or\
           (ambient_light > dusk_treshold and not sunrise <= lokale_Zeit <= experiment_start_time):

            if not Fang_begonnen:
                LepiLED_start()
                append_log("LepiLED eingeschaltet")
                send_lora("LepiLED eingeschaltet")
                Fang_begonnen = True
                UV_active     = True

            _, lokale_Zeit     = Zeit_aktualisieren()
            experiment_start_dt= datetime.strptime(experiment_start_time, "%H:%M:%S")
            lokale_Zeit_dt     = datetime.strptime(lokale_Zeit, "%H:%M:%S")

            Exposure = initial_exposure
            if experiment_start_dt <= lokale_Zeit_dt <= experiment_start_dt + timedelta(hours=1):
                Exposure -= 30

            if LepiLed_end_time <= lokale_Zeit < experiment_end_time:
                Exposure -= 30
                if UV_active:
                    LepiLED_ende()
                    append_log("LepiLED ausgeschaltet")
                    UV_active = False

            code, current_image, Status_Kamera, power_on, Kamera_Fehlerserie = snap_image(
                "tiff", "log", Kamera_Fehlerserie, Exposure
            )

            sensors = read_sensor_data(code, lokale_Zeit)
            sensors.update({"Status_Kamera": Status_Kamera, "Exposure": Exposure})

            if power_on != "---" and sensors["power"] != "---":
                Visible_LED = round((power_on - sensors["power"]) / 1000, 2)
                if Visible_LED > 3:
                    Status_LED = 1
                elif 1 < Visible_LED < 3:
                    error_message(12, Visible_LED)
                    Status_LED = 0
                else:
                    error_message(12, Visible_LED)
                    Status_LED = 0
                sensors.update({"Status_Visible_LED": Status_LED, "Power_Visible_LED": Visible_LED})
            else:
                sensors.update({"Status_Visible_LED": '--', "Power_Visible_LED": '---'})

            sensors["LepiLED"] = "active" if UV_active else "inactive"

            with current_sensor_lock:
                current_sensor_data.clear()
                current_sensor_data.update(sensors)

            csv_path = erstelle_und_aktualisiere_csv(sensors)
            checksum(current_image, algorithm="md5")

            if Kamera_Fehlerserie >= 3:
                error_message(2, "")
                append_log("Beende Aufnahme Schleife. Bereite Neustart vor.")
                checksum(csv_path, algorithm="md5")
                checksum(LOG_PATH, algorithm="md5")
                break

            last_image         = datetime.strptime(lokale_Zeit, "%H:%M:%S")
            next_image         = (last_image + timedelta(minutes=interval)).replace(second=0, microsecond=0)
            _, lokale_Zeit     = Zeit_aktualisieren()
            lokale_Zeit        = datetime.strptime(lokale_Zeit, "%H:%M:%S")
            time_to_next_image = (next_image - lokale_Zeit).total_seconds()
            append_log(f"Warten bis zur nächsten Aufnahme: {round(time_to_next_image)} Sekunden")
            time.sleep(max(time_to_next_image, 0))

        else:
            checksum(csv_path, algorithm="md5")
            append_log("Beende Aufnahme Schleife. Leite zum Ausschalten über")
            checksum(LOG_PATH, algorithm="md5")
            break

# ────── entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    main_loop()
