from Camera import snap_image
from GPIO_Setup import turn_on_led, turn_off_led, button_pressed
from OLED_panel import display_text
import time
from RTC_new_time import set_hwc
from coordinates import set_coordinates
from times import *
from json_read_write import *
import json
from sensor_data import *
from service import *
from log import log_schreiben
from Lights import *
from find_focus import focus
from site_selection import set_location_code
import os
from fram_operations import *
from updater import *
from end import trap_shutdown

latitude, longitude,_,_ = (get_coordinates())
    

def display_sensor_status_with_text(sensor_data, sensor_status):
    """
    Gibt die Sensorinformationen mit display_text aus.
    1. Zeile: Sensorname (wie in sensor_status angegeben)
    2. Zeile: Sensorzustand (OK oder Fehler)
    3. Zeile: Erster Wert, den der Sensor in sensor_data schreibt.

    :param sensor_data: Dictionary mit den Sensor-Daten.
    :param sensor_status: Dictionary mit den Sensor-Status-Werten.
    """
    # Zu überprüfende Sensoren und ihre entsprechenden Datenfelder
    sensors = [
        ("Light_Sensor", "LUX"),
        ("Inner_Sensor", "Temp_in"),
        ("Power_Sensor", "bus_voltage"),
        ("Environment_Sensor", "Temp_out")
    ]

    for sensor_name, data_key in sensors:
        # Sensorzustand prüfen
        status = "OK" if sensor_status.get(sensor_name, 0) == 1 else "Fehler"

        # Sensorwert abrufen
        value = sensor_data.get(data_key, "---")

        # Informationen auf dem Display ausgeben
        display_text(sensor_name, f"Status: {status}", f"Wert: {value}")
        log_schreiben(f"Sensor: {sensor_name},Status: {status}, Wert: {value}")
        time.sleep(4)  # Kurze Pause, damit der Text sichtbar bleibt


Menu_open = False
turn_on_led("blau")
display_text("Menü öffnen:", "bitte Enter drücken", "(rechts unten)")
print("Eingabe Menü mit der Taste Enter ganz rechts unten öffnen")
for _ in range(100):
    if button_pressed("enter"):
        Menu_open =  True
        print("Enter Gedrückt")
        display_text("Eingabe Menü", "geöffnet", "")
        log_schreiben("Lokales User Interface der Falle wurde geöffnet")
        ram_counter(0x0330)

        user = 0
        for _ in range(75):
            if button_pressed("rechts"):
                print("Rechts gedrückt. Öffne Fokusmenü")
                display_text("Fokussierhilfe", "aufgerufen", "")
                log_schreiben("lokale Fokussierhilfe geöffnet")
                focus()
                log_schreiben("Fokussieren beendet")
                user = 1
                
            if button_pressed("enter"):
                display_text("Bitte Land,", "Provinz und","Stadcode wählen")
                log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel geöffnet. Erwarte Neustart nach Ende des Meüpunktes")
                time.sleep(3)
                Neustart = set_location_code()
                if not Neustart:
                    log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel beendet. Es wurden keine Änderungen eingegeben. Fahre fort")   
                    display_text("Code unverändert","fahre fort","")
                    time.sleep(2)        
                if  Neustart:
                    log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel beendet. Es wurden  Änderungen eingegeben. starte neu zum Übernehmen")
                    display_text("Code geändert","Falle startet neu","fürs Anwenden")
                    trap_shutdown(5)
                    
            if button_pressed("oben"):
                print("Oben gedrückt. Öffne Update Menü")
                update()

            time.sleep(.05)
        if not user:
            log_schreiben("Fokus unverändert")
        
        for i in range(5):
            jetzt_local,_ = Zeit_aktualisieren()
            jetzt_local_dt = datetime.strptime(jetzt_local, "%Y-%m-%d %H:%M:%S")  
            display_text("aktuelle Uhrzeit", jetzt_local_dt.strftime("%Y-%m-%d"),jetzt_local_dt.strftime("%H:%M:%S"))
            time.sleep(1)

        display_text("Uhrzeit mit","Enter Taste", "neu stellen")  

        user = 0
        for _ in range(100):
            if button_pressed("enter"):
                log_schreiben("Menü zum aktualisieren der Uhrzeit geöffnet")
                set_hwc()
                for _ in range(5):
                    jetzt_local,_ = Zeit_aktualisieren()
                    jetzt_local_dt = datetime.strptime(jetzt_local, "%Y-%m-%d %H:%M:%S") 
                    display_text("aktuelle Uhrzeit", jetzt_local_dt.strftime("%Y-%m-%d"),jetzt_local_dt.strftime("%H:%M:%S"))
                    time.sleep(1)
                log_schreiben("Menü zum aktualisieren der Uhrzeit geschlossen")
                user = 1
                break
            time.sleep(.05)

                
        if not user:
            log_schreiben("Uhrzeit nicht mit dem lokalen Interface aktualisiert")    
                
                

        display_text("Koordinaten",f"Lat: {latitude}", f"Long: {longitude}")  
        time.sleep(5)
        display_text("Koordinaten mit","Enter Taste", "neu stellen")      

        user = 0
        for _ in range(50):
            if button_pressed("enter"):
                log_schreiben("Menü zum aktualisieren der Koordinaten geöffnet")
                set_coordinates()
                log_schreiben("Menü zum aktualisieren der Koordinaten geschlossen")
                user = 1
                break
            time.sleep(.100) 


        if not user:    
            log_schreiben("Koordinaten nicht mit dem lokalen Interface aktualisiert")  


        display_text("Testlauf starten","","")
        log_schreiben("Starte Systemcheck")

        _,lokale_Zeit = Zeit_aktualisieren() 
        read_sensor_data("Test_hmi",lokale_Zeit) 
        display_sensor_data(sensor_data, sensor_status)  

        display_sensor_status_with_text(sensor_data, sensor_status)   

        display_text("Kamera Test","","")
        time.sleep(1)
        display_text("Kamera Test","aktiviere","UV Lampe")  
        time.sleep(1)  
        LepiLED_start()
        snap_image("jpg","display",0,80)
        LepiLED_ende()
        display_text("Kamera Test","beendet","")   
        time.sleep(1)  

        total_space_gb, used_space_gb, free_space_gb, used_percent, free_percent = get_disk_space()
        display_text("USB Speicher", f"gesamt: {str(total_space_gb)} GB", f"frei:   {str(free_space_gb)} GB")
        log_schreiben(f"USB Speicher: gesamt: {str(total_space_gb)} GB; frei: {str(free_space_gb)} GB")
        time.sleep(3)
        sunset, sunrise, Zeitzone = get_sun()
        sunset = str(sunset)
        sunrise = str(sunrise)
        print(f"Anzeige Dämmerung:{sunset}")
        print(f"Anzeige Dämmerung:{sunrise}")
        display_text("Sonnenuntergang", sunset[:10], sunset[11:19])
        time.sleep(3)
        display_text("Sonnenaufgang", sunrise[:10], sunrise[11:19])
        time.sleep(3)

        display_text("Testlauf beendet","bitte Deckel","schließen") 
        log_schreiben("Beende Systemcheck")
        time.sleep(3)
        break
    
    time.sleep(.05)
if not Menu_open:
    log_schreiben("Falle nicht mit lokalem User Interface parametrisiert")
print("Continue")    