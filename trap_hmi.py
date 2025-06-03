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

def display_sensor_status_with_text(sensor_data, sensor_status):
    """
    Gibt die Sensorinformationen mit display_text aus.
    1. Zeile: Sensorname (wie in sensor_status angegeben)
    2. Zeile: Sensorzustand (OK oder Fehler)
    3. Zeile: Erster Wert, den der Sensor in sensor_data schreibt, inkl. Einheit.
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

if __name__ == "__main__":
 
    Menu_open = False
    turn_on_led("blau")
    try:
        display_text("Menü öffnen:", "bitte Enter drücken", "(rechts unten)")
        print("Eingabe Menü mit der Taste Enter ganz rechts unten öffnen")
        for _ in range(200):
            if button_pressed("enter"):
                Menu_open =  True
                print("Eingabe Menü geöffnet")
                display_text("Eingabe Menü", "geöffnet", "")
                log_schreiben("Lokales User Interface der Falle wurde geöffnet")
                try:
                    ram_counter(0x0330)
                except:
                    pass    

                user = 0
                for _ in range(75):
                    if button_pressed("rechts"):
                        print("Rechts gedrückt. Öffne Fokusmenü")
                        log_schreiben("lokale Fokussierhilfe geöffnet")
                        focus()
                        turn_off_led("gelb")
                        log_schreiben("Fokussieren beendet")
                        user = 1
                        
                    if button_pressed("unten"):
                        display_text("Bitte Land,", "Provinz und","Stadcode wählen",3)
                        log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel geöffnet. Erwarte Neustart nach Ende des Meüpunktes")
                        Neustart = set_location_code()
                        if not Neustart:
                            log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel beendet. Es wurden keine Änderungen eingegeben. Fahre fort")   
                            display_text("Code unverändert","fahre fort","",2)
                            user = 1
                            turn_off_led("blau")       
                        if  Neustart:
                            log_schreiben("Menü zum Ändern der Provinz und Stadtkürzel beendet. Es wurden  Änderungen eingegeben. starte neu zum Übernehmen")
                            display_text("Code geändert","Falle startet neu","fürs Anwenden",3)
                            turn_off_led("blau")
                            
                    if button_pressed("oben"):
                        print("Oben gedrückt. Öffne Update Menü")
                        turn_off_led("blau")
                        update()
                        log_schreiben("fahre fort")
                        user = 1

                    time.sleep(.05)
                if not user:
                    log_schreiben("kein Verstecktes Menü geöffnet")
                turn_off_led("blau")

                display_text("Datum / Uhrzeit:","hoch aktualisieren","runter bestätigen",3) 
                turn_on_led("blau")                
                user_selection_time = False
                print("Zeitmenü anfang")
                while not user_selection_time:
                    jetzt_local,_ = Zeit_aktualisieren()
                    jetzt_local_dt = datetime.strptime(jetzt_local, "%Y-%m-%d %H:%M:%S") 
                    display_text(jetzt_local_dt.strftime("%Y-%m-%d"),jetzt_local_dt.strftime("%H:%M:%S"),"▲ = neu  ▼ = ok")
                    for _ in range(20):
                        if button_pressed("oben"):
                            turn_off_led("blau")
                            log_schreiben("Menü zum aktualisieren der Uhrzeit geöffnet")
                            time.sleep(1)
                            set_hwc()
                            log_schreiben("Menü zum aktualisieren der Uhrzeit geschlossen")
                            user_selection_time = True
                            
                        if button_pressed("unten"):
                            log_schreiben("Uhrzeit nicht mit dem lokalen Interface aktualisiert")  
                            turn_off_led("blau")
                            user_selection_time = True
                                   
                print("Zeitmenü Ende")        
                        
                latitude, longitude,_,_ = (get_coordinates())       
                display_text("Koordinaten mit","hoch aktualisieren","runter bestätigen",3)
                display_text(f"N-S: {latitude}", f"O-W: {longitude}", "▲ = neu  ▼ = ok",0)
                turn_on_led("blau")
                user_selection_GPS = False
                print("GPS Menü Anfang") 
                while not user_selection_GPS:
                    if button_pressed("oben"):
                        turn_off_led("blau")
                        log_schreiben("Menü zum aktualisieren der Koordinaten geöffnet")
                        time.sleep(1)
                        set_coordinates()
                        log_schreiben("Menü zum aktualisieren der Koordinaten geschlossen")
                        user_selection_GPS = True
                        
                    if button_pressed("unten"):
                        log_schreiben("Koordinaten nicht mit dem lokalen Interface aktualisiert")  
                        turn_off_led("blau")
                        user_selection_GPS = True
                        
                    time.sleep(.05) 
                    

                display_text("Testlauf starten","","",2)
                log_schreiben("Starte Systemcheck")

                _,lokale_Zeit = Zeit_aktualisieren() 
                read_sensor_data("Test_hmi",lokale_Zeit) 
                display_sensor_data(sensor_data, sensor_status)  

                display_sensor_status_with_text(sensor_data, sensor_status)   
                

                display_text("Kamera Test","","",1)
                Status_Kamera = 0
                while Status_Kamera == 0:
                    
                    display_text("Kamera Test","aktiviere","UV Lampe",1)  
                    LepiLED_start()
                    try:
                        _, _, Status_Kamera, _, _ = snap_image("jpg","display",0,80)
                    except:
                        pass
                    LepiLED_ende()
                    time.sleep(1)
                    print(f"Kamera Status: {Status_Kamera}")
                    if Status_Kamera == 0:
                        display_text("Kamera Test","Fehler- Falle","wiederhohlt Test",3)
                display_text("Kamera Test","erfolgreich","beendet",3)   

                USB = 0
                while USB == 0:
                    total_space_gb = None
                    total_space_gb, used_space_gb, free_space_gb, _, _ = get_disk_space()
                    display_text("USB Speicher", f"gesamt: {str(total_space_gb)} GB", f"frei:   {str(free_space_gb)} GB",3)
                    log_schreiben(f"USB Speicher: gesamt: {str(total_space_gb)} GB; frei: {str(free_space_gb)} GB")
                    if total_space_gb is None:
                        display_text("USB Speicher","nicht erkannt","Prüfe Anschluss",3)
                        trap_shutdown(5)
                    elif free_space_gb < 13:
                        display_text("USB Speicher","fast voll","bitte leeren",3)
                        log_schreiben("USB Speicher fast voll, bitte leeren")
                        trap_shutdown(5)
                    elif free_space_gb >= 13:
                        display_text("USB Speicher","OK","",1)
                        log_schreiben("USB Speicher OK")
                        USB = 1   
                    time.sleep(.05)    
                
                sunset, sunrise, Zeitzone = get_sun()
                sunset = str(sunset)
                sunrise = str(sunrise)
                print(f"Anzeige Dämmerung:{sunset}")
                print(f"Anzeige Dämmerung:{sunrise}")
                display_text("Sonnenuntergang", sunset[:10], sunset[11:19],3)
                display_text("Sonnenaufgang", sunrise[:10], sunrise[11:19],3)
                
                try:
                    sn = read_fram(0x0110, 8).strip()
                    display_text("Seriennummer", sn, "",2)
                except Exception as e:
                    error_message(9,e)
                    sn = get_value_from_section("/home/Ento/serial_number.json", "general", "serielnumber")
                    display_text("Seriennummer", sn, "",2)
                    
                display_text("Testlauf beendet","bitte Deckel","schließen",2) 
                log_schreiben("Beende Systemcheck")
                break
            
            time.sleep(.05)
        if not Menu_open:
            log_schreiben("Falle nicht mit lokalem User Interface parametrisiert")
            
             
    except:
        for i in range(5): 
            turn_on_led("rot")
            turn_on_led("gelb")
            time.sleep(0.5)
            turn_off_led("rot")
            time.sleep(0.5)   
            turn_off_led("gelb")  
    
    print("Continue")             