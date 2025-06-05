from Lights import *
from Camera import snap_image
from sensor_data import read_sensor_data
from times import *
from json_read_write import *
from service import *
from log import log_schreiben
from csv_handler import erstelle_und_aktualisiere_csv
from json_read_write import get_value_from_section
from Lights import *
from lora import send_lora
from error_handling import error_message
import shutil
import os
from datetime import timedelta, datetime
from wait import wait 
from fram_operations import *
import struct
import time

print("starte Capturing")  
wait()
log_schreiben("Beginne Daten und Bildaufnahme")
try: 
    total_space_gb, used_space_gb, free_space_gb, used_percent, free_percent = get_disk_space()
    log_schreiben(f"USB Speicher gesamt: {total_space_gb} GB")
    log_schreiben(f"USB Speicher belegt: {used_space_gb} GB  {used_percent} %")
    log_schreiben(f"USB Speicher frei:   {free_space_gb} GB  {free_percent} %")

except Exception as e:
    error_message(3,e)

try:
    send_lora(f"USB Speicher gesamt: {total_space_gb} GB\nUSB Speicher belegt: {used_space_gb} GB)\nUSB Speicher frei:   {free_space_gb} GB")
except:
    print(f"USB Speicherdaten nicht gesendet")
    pass

try: 
    # Schreibe freien Speicher als Float (4 Bytes) ins FRAM
    write_fram_bytes(0x0390, struct.pack('f', free_space_gb))
    print(f"freien Speicher im Ram gemerkt:{free_space_gb}")
except Exception as e:
    print(f"Fehler beim Schreiben des freien Speichers in den RAM: {e}")

experiment_start_time, experiment_end_time, LepiLed_end_time, _, _ = get_experiment_times()
_, sunrise, _ = get_sun()
sunrise = sunrise.strftime('%H:%M:%S')

try:
    dusk_treshold = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "dusk_treshold")
    interval = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "interval")
    initial_exposure = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "initial_exposure")
except Exception as e:
    error_message(11,e)
    

Fang_begonnen = False
UV_active = False
Kamera_Fehlerserie = 0

print("LepiLED aus:", LepiLed_end_time)
print("Beginne Schleife", experiment_start_time)
print("beende Schleife:", experiment_end_time)


try:
    ordner = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_folder")
    Dateiname = os.path.basename(ordner)
    zieldatei = os.path.join(ordner, f"{Dateiname}_Kameraeinstellungen.xml")
    shutil.copy("/home/Ento/LepmonOS/Kamera_Einstellungen.xml", zieldatei)
    checksum(zieldatei, algorithm="md5")
    print("Kameraeinstellungen kopiert")
except Exception as e:
    print(f"Fehler beim Kopieren der Kameraeinstellungen: {e}")

while True:
    _, lokale_Zeit,_ = Zeit_aktualisieren()
    sensors = read_sensor_data("check Lux", lokale_Zeit)
    ambient_light = sensors["LUX"]

    if (ambient_light <= dusk_treshold and not experiment_end_time <= lokale_Zeit <= experiment_start_time) or\
       (ambient_light > dusk_treshold and not sunrise <= lokale_Zeit <= experiment_start_time):

        if not Fang_begonnen:
            LepiLED_start()
            log_schreiben("LepiLED eingeschaltet")
            log_schreiben("------------------")
            send_lora("LepiLED eingeschaltet")
            Fang_begonnen = True
            UV_active = True

        RPI_time()
            
        experiment_start_string = datetime.strptime(experiment_start_time, "%H:%M:%S")
        lokale_Zeit_string = datetime.strptime(lokale_Zeit, "%H:%M:%S")
        print(f"exp start string {experiment_start_string}")
        print(lokale_Zeit_string)
        
        Exposure = initial_exposure
        if experiment_start_string <= lokale_Zeit_string <= experiment_start_string + timedelta(hours=1):
            Exposure = initial_exposure - 30

        if LepiLed_end_time <= lokale_Zeit < experiment_end_time:
            Exposure = initial_exposure - 30
            if UV_active:
                LepiLED_ende()
                log_schreiben("LepiLED ausgeschaltet")
                send_lora("LepiLED ausgeschaltet")
                UV_active = False  
        
        code, current_image, Status_Kamera, power_on, Kamera_Fehlerserie = snap_image("tiff", "log", Kamera_Fehlerserie, Exposure)
        sensors = read_sensor_data(code, lokale_Zeit)
        sensors["Status_Kamera"] = Status_Kamera
        sensors["Exposure"] = Exposure
        print(power_on)
        if not power_on == "---" and not sensors["power"] == "---":
            Visible_LED = round((power_on - sensors["power"]) / 1000, 2)          
        
            if Visible_LED > 3:
                Status_LED = 1
            elif 1 < Visible_LED < 3:
                error_message(12, Visible_LED)
                Status_LED = 0
            elif 1 > Visible_LED:
                error_message(12, Visible_LED)
                Status_LED = 0 

            sensors["Status_Visible_LED"] = Status_LED 
            sensors["Power_Visible_LED"] = Visible_LED
            
        if power_on == "---" or sensors["power"] == "---":
            sensors["Status_Visible_LED"] = '--' 
            sensors["Power_Visible_LED"] = '---'
            
        if UV_active:
            sensors["LepiLED"] = "active" 
        elif not UV_active:
            sensors["LepiLED"] = "inactive"                                        

        csv_path = erstelle_und_aktualisiere_csv(sensors)

        checksum(current_image, algorithm="md5")

        if Kamera_Fehlerserie >= 3:
            error_message(2, "")
            print("Beende Aufnahme Schleife\nLeite zum Ausschalten über")
            log_schreiben("Beende Aufnahme Schleife. Bereite Neustart vor.")
            log_schreiben("Fahre Falle in 1 Minute herunter und startet neu")
            checksum(csv_path, algorithm="md5")
            log_path = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_log")
            checksum(log_path, algorithm="md5")
            break              

        last_image = datetime.strptime(lokale_Zeit, "%H:%M:%S")
        next_image = (last_image + timedelta(minutes=interval)).replace(second=0, microsecond=0)
        _, lokale_Zeit,_ = Zeit_aktualisieren()
        lokale_Zeit = datetime.strptime(lokale_Zeit, "%H:%M:%S")
        time_to_next_image = (next_image - lokale_Zeit).total_seconds()

        log_schreiben(f"Warten bis zur nächsten Aufnahme: {round(time_to_next_image,0)} Sekunden")
        print(f"Warten bis zur nächsten Aufnahme: {round(time_to_next_image,0)} Sekunden")
        if time_to_next_image > 0:
            time.sleep(time_to_next_image)

    elif (ambient_light > dusk_treshold and sunrise <= lokale_Zeit <= experiment_start_time) or\
         (experiment_end_time <= lokale_Zeit <= experiment_start_time):
        try:
            checksum(csv_path, algorithm="md5")
        except Exception as e:
            print(f"Checksumme der Metadatentabelle nicht erstellt, da diese nicht existiert: {e}")
        log_path = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_log")
        print("Beende Aufnahme Schleife\nLeite zum Ausschalten über")
        log_schreiben("------------------")
        _, _, free_space_gb_after_run, _, _ = get_disk_space()
        try:
            # Lese die 4 Bytes Float aus dem FRAM und rechne mit aktuellem Wert
            free_space_before_run_bytes = read_fram_bytes(0x0390, 4)
            free_space_before_run = struct.unpack('f', free_space_before_run_bytes)[0]
            size = free_space_before_run - free_space_gb_after_run
            size_rounded = round(size, 1)
            log_schreiben(f"in dieser Nacht wurden {size_rounded} GB an Daten generiert")
            send_lora(f"in dieser Nacht wurden {size_rounded} GB an Daten generiert")
        except Exception as e:
            print(f"Kein Ram vorhanden. verbrauchter Speicher nicht gemessen:{e}")    
            log_schreiben("Kein Ram vorhanden. verbrauchter Speicher nicht gemessen")
            pass
        log_schreiben("Beende Aufnahme Schleife. Leite zum Ausschalten über")
        log_schreiben("Fahre Falle in 1 Minute herunter und startet neu")
        checksum(log_path, algorithm="md5")

        break
    
print("hauptschleife beendet")