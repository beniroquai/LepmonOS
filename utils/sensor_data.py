import adafruit_bh1750      #Lichtsensor
import bme280               #Außensensor
from .ina226 import INA226   #Strommesser
import adafruit_pct2075     #Innensensor
import time
import board
import busio
import smbus2
import json
import os
import logging
from utils.service import log_schreiben
from utils.json_read_write import get_value_from_section, get_config_path
from utils.error_handling import error_message

from utils.times import *


os.system('sudo raspi-config nonint do_i2c 0') # I2C aktivieren
i2c = busio.I2C(board.SCL, board.SDA)

port = 1
address = 0x76
bus = smbus2.SMBus(port)

sensor_data = {}
sensor_status = {}
def update_sensor_data(lib,key, value):
    lib[key] = value


def read_sensor_data(code,lokale_Zeit):
    try:
        Dämmerungsschwellenwert = get_value_from_section(get_config_path("Lepmon_config.json"), "capture_mode", "dusk_treshold")
    except Exception as e:
        error_message(11,e)
    update_sensor_data(sensor_data, "code", code)
    update_sensor_data(sensor_data, "time_read", lokale_Zeit)
    update_sensor_data(sensor_status, "time_read", lokale_Zeit)

    try:
        LUX = adafruit_bh1750.BH1750(i2c)
        LUX = round(LUX.lux, 2)
        Sensorstatus_Licht = 1
    except Exception as e:
        error_message(4,e)

        Sensorstatus_Licht = 0
        LUX = Dämmerungsschwellenwert

    update_sensor_data(sensor_data, "LUX", LUX)
    update_sensor_data(sensor_status, "Light_Sensor", Sensorstatus_Licht)

    try:
        Temp_in = adafruit_pct2075.PCT2075(i2c)
        Temp_in = round(Temp_in.temperature, 2)
        Sensorstatus_Inne = 1
    except Exception as e:
        error_message(6,e)

        Temp_in = "---"
        Sensorstatus_Inne = 0
    update_sensor_data(sensor_data, "Temp_in", Temp_in)
    update_sensor_data(sensor_data, "Inner_Sensor", Sensorstatus_Inne)
    update_sensor_data(sensor_status, "Inner_Sensor", Sensorstatus_Inne)

    try:
        ina = INA226(busnum=1, max_expected_amps=10, log_level=logging.INFO)
        ina.configure()
        ina.set_low_battery(5)
        Sensorstatus_Strom = 1

        ina.wake(3)
        time.sleep(0.2)

        bus_voltage = round(ina.voltage(), 2)
        shunt_voltage = round(ina.shunt_voltage(), 2)
        current = round(ina.current(), 2)
        power = round(ina.power(), 2)

    except Exception as e:
        error_message(7,e)
        bus_voltage = "---"
        shunt_voltage = "---"
        current = "---"
        power = "---"
        Sensorstatus_Strom = 0
    update_sensor_data(sensor_data, "bus_voltage", bus_voltage)
    update_sensor_data(sensor_data, "shunt_voltage", shunt_voltage)
    update_sensor_data(sensor_data, "current", current)
    update_sensor_data(sensor_data, "power", power)
    update_sensor_data(sensor_data, "Power_Sensor", Sensorstatus_Strom)
    update_sensor_data(sensor_status, "Power_Sensor", Sensorstatus_Strom)

    try:
        calibration_params = bme280.load_calibration_params(bus, address)
        Außensensor = bme280.sample(bus, address, calibration_params)
        Temperatur = round(Außensensor.temperature, 2)
        Luftdruck = round(Außensensor.pressure, 2)
        Luftfeuchte = round(Außensensor.humidity, 2)
        Status_außen = 1
    except Exception as e:
        error_message(5,e)
        Temperatur = "---"
        Luftdruck = "---"
        Luftfeuchte = "---"
        Status_außen = 0
        pass
    update_sensor_data(sensor_data, "Temp_out", Temperatur)
    update_sensor_data(sensor_data, "air_pressure", Luftdruck)
    update_sensor_data(sensor_data, "air_humidity", Luftfeuchte)
    update_sensor_data(sensor_data, "Environment_Sensor", Status_außen)
    update_sensor_data(sensor_status, "Environment_Sensor", Status_außen)

    # Rückgabe der Sensordaten
    return sensor_data

def write_sensor_data_to_json(sensor_data,sensor_status):
    file_path_data = get_config_path("sensor_values.json")  # Datei im gleichen Ordner
    file_path_status = get_config_path("sensor_status.json")

    try:
        with open(file_path_data, "w") as json_file:
            json.dump(sensor_data, json_file, indent=4)  # Daten in JSON schreiben
        print(f"Sensor-Daten erfolgreich in {file_path_data} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Schreiben der Sensor-Daten in die JSON-Datei: {e}")

    try:
        with open(file_path_status, "w") as json_file:
            json.dump(sensor_status, json_file, indent=4)  # Daten in JSON schreiben
        print(f"Sensor-Daten erfolgreich in {file_path_status} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Schreiben der status-Daten in die JSON-Datei: {e}")        


def display_sensor_data(sensor_data, sensor_status):
    """
    Liest die Dictionaries sensor_data und sensor_status und gibt die Inhalte im Terminal aus.
    Überprüft außerdem, ob in sensor_status Werte 0 enthalten sind, und gibt die betroffenen Sensoren aus.

    :param sensor_data: Dictionary mit den Sensor-Daten.
    :param sensor_status: Dictionary mit den Sensor-Status-Werten.
    """
    # Sensor-Daten ausgeben
    print("Sensor-Daten:")
    for key, value in sensor_data.items():
        print(f"{key}: {value}")

    print("\nSensor-Status:")
    for key, value in sensor_status.items():
        print(f"{key}: {value}")

    # Überprüfung der Sensor-Status-Werte
    print("\nÜberprüfung der Sensorstatus:")
    all_ok = True
    for key, value in sensor_status.items():
        if value == 0:
            print(f"Sensor '{key}' hat den Wert 0.")
            all_ok = False

    if all_ok:
        print("Alle Sensorstatus-Werte sind 1.")
    else:
        print("Mindestens ein Sensor hat den Wert 0.")

        
if __name__ == "__main__":
    _, lokale_Zeit = Zeit_aktualisieren()
    read_sensor_data(lokale_Zeit)
    for key, value in sensor_data.items():
        print(f"{key}: {value}")
    #write_sensor_data_to_json(sensor_data)    
    time.sleep(3)  # Sleep for a second before the next read 