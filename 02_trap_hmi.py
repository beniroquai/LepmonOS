from utils.Camera import snap_image
from utils.GPIO_Setup import turn_on_led, turn_off_led, button_pressed
from utils.OLED_panel import display_text
from utils.RTC_new_time import set_hwc
from utils.coordinates import set_coordinates
from utils.times import *
from utils.json_read_write import *
from utils.sensor_data import *
from utils.service import *
from utils.log import log_schreiben
from utils.Lights import *
from utils.find_focus import focus
from utils.site_selection import set_location_code
from utils.wait import wait 
from utils.fram_operations import *
from utils.updater import update
from utils.end import trap_shutdown 

import json
import time
import os

latitude, longitude,_,_ = (get_coordinates())
    

def display_sensor_status_with_text(sensor_data, sensor_status):
    """
    Gibt die Sensorinformationen mit display_text aus.
    1. Zeile: Sensorname (wie in sensor_status angegeben)
    2. Zeile: Sensorzustand (OK oder Fehler)
    3. Zeile: Erster Wert, den der Sensor in sensor_data schreibt, inkl. Einheit.

    :param sensor_data: Dictionary mit den Sensor-Daten.
    :param sensor_status: Dictionary mit den Sensor-Status-Werten.
    """
    # Sensoren, Datenfeld und Einheit
    sensors = [
        ("Light_Sensor", "LUX", "Lux"),
        ("Inner_Sensor", "Temp_in", "°C"),
        ("Power_Sensor", "bus_voltage", "V"),
        ("Environment_Sensor", "Temp_out", "°C")
    ]

    for sensor_name, data_key, einheit in sensors:
        status_value = sensor_status.get(sensor_name, 0)
        status = "OK" if str(status_value) == "1" or status_value == 1 else "Fehler"
        value = sensor_data.get(data_key, "---")
        # Wert und Einheit zusammen anzeigen
        display_text(sensor_name, f"Status: {status}", f"Wert: {value} {einheit}",2.5)
        log_schreiben(f"Sensor: {sensor_name},Status: {status}, Wert: {value} {einheit}")

        # Informationen auf dem Display ausgeben
        display_text(sensor_name, f"Status: {status}", f"Wert: {value}")
        log_schreiben(f"Sensor: {sensor_name},Status: {status}, Wert: {value}")
        time.sleep(4)  # Kurze Pause, damit der Text sichtbar bleibt


Menu_open = False
turn_on_led("blau")
display_text("Menü öffnen", "bitte rechte Taste", "drücken")
print("Eingabe Menü mit der Taste Enter ganz rechts öffnen")
for _ in range(100): #200
    if button_pressed("enter"):
        Menu_open =  True
        print("Enter Gedrückt")
        display_text("Eingabe Menü", "geöffnet", "")
        log_schreiben("Lokales User Interface der Falle wurde geöffnet")

        user = 0
        for _ in range(75):
            if button_pressed("rechts"):
                print("Rechts gedrückt. Öffne Fokusmenü")
                display_text("Fokussierhilfe", "aufgerufen", "")
                log_schreiben("lokale Fokussierhilfe geöffnet")
                focus()
                log_schreiben("Fokussieren beendet")
                user = 1
                
            if button_pressed("oben"):
                print("Oben gedrückt. Öffne Update Menü")
                display_text("Update Menü", "geöffnet", "")
                log_schreiben("Update Menü geöffnet")
                try:
                    ram_counter(0x0330)
                except:
                    pass
                try:
                    update()
                except Exception as e:
                    print(f"Update menu error: {e}")
                    display_text("Update Fehler", "Versuche später", "erneut")
                    time.sleep(3)
                log_schreiben("Update Menü geschlossen, fahre fort")
                user = 1
                
            if button_pressed("enter"):
                display_text("Bitte Land,", "Provinz und","Stadcode wählen")
                log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel geöffnet. Erwarte Neustart nach Ende des Meüpunktes")
                time.sleep(3)
                Neustart = set_location_code()
                if not Neustart:
                    log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel beendet. Es wurden keine Änderungen eingegeben. Fahre fort")           
                if  Neustart:
                    log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel beendet. Es wurden  Änderungen eingegeben. starte neu zum Übernehmen")
                    t = 5
                    for _ in range(5):
                        display_text("Code geändert","Falle startet neu",f"fürs Anwenden {t}")
                        t -=1
                        time.sleep(1)
                    display_text("","","")    
                    os.system('sudo reboot')
                              
                              
            time.sleep(.05)
        if not user:
            log_schreiben("Fokus unverändert")
            

        jetzt_local,_ = Zeit_aktualisieren()
        for i in range(5):
            _,lokale_Zeit = Zeit_aktualisieren()    
            display_text("aktuelle Uhrzeit", jetzt_local,"")
            time.sleep(1)

        display_text("Uhrzeit mit","rechter Taste", "neu stellen")  

        user = 0
        for _ in range(100):
            if button_pressed("enter"):
                log_schreiben("Menü zum aktualisieren der Uhrzeit geöffnet")
                set_hwc()
                log_schreiben("Menü zum aktualisieren der Uhrzeit geschlossen")
                user = 1
                break
            time.sleep(.05)

                
        if not user:
            log_schreiben("Uhrzeit nicht mit dem lokalen Interface aktualisiert")    
                
                

        display_text("Koordinaten",f"Lat: {latitude}", f"Long: {longitude}")  
        time.sleep(5)
        display_text("Koordinaten mit","rechter Taste", "neu stellen")      
        
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
        display_text("Kamera Test","erfolgreich","beendet")     

        total_space_gb, used_space_gb, free_space_gb, used_percent, free_percent = get_disk_space()
        display_text("USB Speicher", f"gesamt: {str(total_space_gb)} GB", f"frei:   {str(free_space_gb)} GB")
        log_schreiben(f"USB Speicher: gesamt: {str(total_space_gb)} GB; frei: {str(free_space_gb)} GB")
        time.sleep(3)
        sunset, sunrise, Zeitzone = get_sun()
        sunset = str(sunset)
        sunrise = str(sunrise)
        print(f"Anzeige Dämmerung:{sunset}")
        print(f"Anzeige Dämmerung:{sunrise}")       
        display_text("Sonnenuntergang",sunset,"")   
        time.sleep(3)
        display_text("Sonnenaufgang",sunrise,"")   
        time.sleep(3)   

        display_text("Testlauf erfolgreich","bitte Deckel","schließen") 
        log_schreiben("Beende Systemcheck")
        time.sleep(3)
        break
    
    time.sleep(.05)
if Menu_open:
    log_schreiben("Falle nicht mit lokalem User Interface parametrisiert")
print("Continue with wait")    
wait()