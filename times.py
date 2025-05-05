from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
import pytz
import ephem
from log import log_schreiben
from error_handling import error_message
from json_read_write import *
import time
import time
import board
import adafruit_ds3231
import subprocess

i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

def Zeit_aktualisieren():
    
    t = rtc.datetime
    dt = datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    jetzt_local = dt.strftime("%Y-%m-%d %H:%M:%S")
    lokale_Zeit = dt.strftime("%H:%M:%S")
    try:
        subprocess.run(['sudo', 'date', "-s", jetzt_local])
        print(f"Uhrzeit des Pi auf {jetzt_local} gestellt")
    except Exception as e:
        print(f"Fehler beim Stellen der RPi Uhr: {e}")
        
    return jetzt_local, lokale_Zeit

def berechne_zeitzone(latitude,longitude):
    latitude, longitude,_,_ = (get_coordinates())    

    tf = TimezoneFinder()
    
    zeitzone_name = tf.timezone_at(lat=latitude, lng=longitude) # Finde die Zeitzone basierend auf den Koordinaten
    
    if zeitzone_name is None:
        print("Keine Zeitzone gefunden für diese Koordinaten.")
        return None
    
    # Hole das aktuelle Datum und die Uhrzeit in der gefundenen Zeitzone
    Zeitzone = pytz.timezone(zeitzone_name)

    return Zeitzone


def get_sun():
    jetzt_local = datetime.now()
    try:
        latitude, longitude,_,_ = (get_coordinates())
    except Exception as e:
        error_message(11,e)
    Zeitzone = berechne_zeitzone(latitude, longitude)
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)

    jetzt_local_utc = jetzt_local.astimezone(pytz.utc)
    
    sunset = ephem.localtime(observer.next_setting(ephem.Sun(), start=jetzt_local_utc)) # Calculate times based on UTC time
    
    next_day = jetzt_local + timedelta(days=1)# For the following day
    next_day_utc = next_day.astimezone(ephem.UTC)

    sunrise = ephem.localtime(observer.previous_rising(ephem.Sun(), start=next_day_utc))

    return sunset, sunrise, Zeitzone
    # times, at which the sun passes the horizon


def get_experiment_times():
    try:
        latitude, longitude,_,_ = (get_coordinates()) 
        lepi_led_buffer = timedelta(minutes=int(get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "LepiLed_buffer")))
        time_buffer = timedelta(minutes=int(get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "time_buffer")))  
    except Exception  as e:
        error_message(11,e)
    
    jetzt_local, _ = Zeit_aktualisieren()  # Nur das erste Element des Tupels verwenden
    sunset, sunrise, _ = get_sun()
    
    # Berechnung der Zeiten für Dämmerung und Morgendämmerung
    
    dusk_time = sunset - time_buffer
    dawn_time = sunrise + time_buffer
    LepiLed_end_time = sunrise - lepi_led_buffer

    experiment_start_time = dusk_time.replace(tzinfo=None)
    experiment_start_time = experiment_start_time.strftime("%H:%M:%S")

    experiment_end_time = dawn_time.replace(tzinfo=None)
    experiment_end_time = experiment_end_time.strftime("%H:%M:%S")

    LepiLed_end_time = LepiLed_end_time.replace(tzinfo=None)
    LepiLed_end_time = LepiLed_end_time.strftime("%H:%M:%S")
    
    return experiment_start_time, experiment_end_time, LepiLed_end_time, time_buffer, lepi_led_buffer
    # times for start and stop while loop in main script. additionally, LepiLed is switched off 1h before end


def get_times_power():
    latitude, longitude,_,_ = (get_coordinates()) 

    time_buffer = timedelta(minutes=int(get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "time_buffer")))
    jetzt_local, _ = Zeit_aktualisieren()  # Nur das erste Element des Tupels verwenden
    sunset, sunrise, _ = get_sun()
    
    # Berechnung der Zeiten für Dämmerung und Morgendämmerung
    power_on = sunset - time_buffer - timedelta(minutes=15)
    power_off = sunrise + time_buffer + timedelta(minutes=1)

    power_on = power_on.replace(tzinfo=None)
    power_on = power_on.strftime('%Y-%m-%d %H:%M:%S')

    power_off = power_off.replace(tzinfo=None)
    power_off = power_off.strftime('%Y-%m-%d %H:%M:%S')
    
    return power_on, power_off
    #times to write into FRam for power management 

if __name__ == "__main__":
    jetzt_local, lokale_Zeit = Zeit_aktualisieren()
    print("Aktuelle Zeit:", jetzt_local)
    print("Aktuelle lokale Zeit:", lokale_Zeit)
          