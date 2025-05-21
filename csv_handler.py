import os
import csv
from json_read_write import get_value_from_section
from datetime import datetime
from times import *
from error_handling import error_message

def erstelle_und_aktualisiere_csv(sensor_data):
    try:
        dusk_treshold = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "dusk_treshold")
        interval = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "capture_mode", "interval")
        sensor_id = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "serielnumber")    
        path = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_folder")
    except Exception as e:
        error_message(11,e)
    csv_name = f"{os.path.basename(path)}.csv"
    csv_path = os.path.join(path, csv_name)

    ### Metadata
    jetzt_local, lokale_Zeit = Zeit_aktualisieren()
    latitude, longitude, _, _ = get_coordinates()

    sunset, sunrise, _ = get_sun()
    experiment_start_time, experiment_end_time, LepiLed_end_time,_,_ = get_experiment_times()

    ### Dateikopf
    try:
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter='\t')  # Setze den Tabulator als Trennzeichen
                csv_writer.writerow(["#UTC Time:",                  jetzt_local])
                csv_writer.writerow(["#Longitude:",                 longitude]) 
                csv_writer.writerow(["#Latitude:",                  latitude])
                csv_writer.writerow([])
                csv_writer.writerow(["#Sonnenuntergang:",           sunset.strftime("%H:%M:%S")])
                csv_writer.writerow(["#Sonnenaufgang:",             sunrise.strftime("%H:%M:%S")])
                csv_writer.writerow([])
                csv_writer.writerow(["#Beginn Monitoring:",         experiment_start_time])
                csv_writer.writerow(["#Ende Monitoring:",           experiment_end_time])
                csv_writer.writerow(["#Ausschalten der LepiLED:",   LepiLed_end_time])
                csv_writer.writerow([])
                csv_writer.writerow(["#Machine ID:",                sensor_id])
                csv_writer.writerow(["#Dämmerungs Schwellenwert:",  dusk_treshold])
                csv_writer.writerow(["#Aufnahme Intervall:",        interval])
                csv_writer.writerow([])
                csv_writer.writerow(["********************"])
                csv_writer.writerow([])
                csv_writer.writerow(["#Starting new Programme"])
                csv_writer.writerow(["#Local Time:", lokale_Zeit])
                csv_writer.writerow([])

                # Schreibe die Überschrift (Keys von sensor_data)
                csv_writer.writerow(sensor_data.keys())

        # Schreibe die Sensordaten
        with open(csv_path, mode='a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter='\t')

            # Schreibe die Überschrift, falls die Datei leer ist
            if os.path.getsize(csv_path) == 0:
                csv_writer.writerow(sensor_data.keys())

            # Schreibe die Sensordaten
            csv_writer.writerow(sensor_data.values())

        return csv_path
    
    except Exception as e:
        error_message(13,e)


if __name__ == "__main__":
   print("CSV Handler")