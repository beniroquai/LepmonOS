from times import get_times_power
from OLED_panel import display_text, display_text_and_image
from service import *
from log import log_schreiben
from lora import send_lora
from error_handling import *
import time
from times import *
from json_read_write import *
from Lights import dim_down
from RTC_alarm import set_alarm
from fram_operations import *
from service import *
from runtime import on_start
from GPIO_Setup import turn_off_led
from end import trap_shutdown




if __name__ == "__main__":
    dim_down()
    turn_off_led("blau")
    print("starte Setup")      
    RPI_time()
    on_start()
    
    Version = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "version")
    date = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "date") 
    display_text_and_image("Will-","kommen", Version, "/home/Ento/LepmonOS/startsequenz/Logo_1_9.png",1)
    print("Wilkommen message 1 in Display")

    sn = None
    while sn == None:
        try:
            time.sleep(2)
            sn = read_fram(0x0110, 8).strip()
            print(f"Serial Number from FRAM: {sn}")    
        except Exception as e:
            print("sn nicht vom Fram gelesen. nutze externe Datei")
            sn = get_value_from_section("/home/Ento/serial_number.json", "general", "serielnumber")
            print(f"Serial Number from JSON: {sn}")
        time.sleep(1)
    display_text_and_image("Will-","kommen", Version, "/home/Ento/LepmonOS/startsequenz/Logo_2_9.png") 
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "serielnumber", sn)

    send_lora("Starte Lepmon Software")
    
    try:
        ram_counter(0x0310)
    except Exception as e:
        print(f"Fehler beim Lesen des RAM-Counters: {e}")

    set_serial_number()
    delete_error_code()
    display_text_and_image("Will-","kommen", Version, "/home/Ento/LepmonOS/startsequenz/Logo_3_9.png")    

  

    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_folder", "")
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_log", "")
    print("Konfigurationsdatei zurückgesetzt")
    
    for i in range(4, 6):
        display_text_and_image("Will-","kommen", Version, f"/home/Ento/LepmonOS/startsequenz/Logo_{i}_9.png",1)

    ordner = erstelle_ordner()
    if ordner == None:
        display_text("USB Stick","nicht erkannt","neu einstecken",3)
        trap_shutdown(60)
        
    initialisiere_logfile()

        
    display_text_and_image("Will-","kommen", Version, "/home/Ento/LepmonOS/startsequenz/Logo_7_9.png",1)

    log_schreiben(f"Software- Version: {Version} vom {date}")
    log_schreiben("Experiment Parameter:")


    send_lora("Berechne Zeiten für Power Managament")
    sunset, sunrise, Zeitzone = get_sun()


    log_schreiben(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}")
    log_schreiben(f"Sonnenaufgang:   {sunrise.strftime('%H:%M:%S')}")

    send_lora(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}\nSonnenaufgang: {sunrise.strftime('%H:%M:%S')}")
    display_text_and_image("Will-","kommen", Version, "/home/Ento/LepmonOS/startsequenz/Logo_8_9.png",1)  
    power_on, power_off = get_times_power()

    log_schreiben(f"Zeit für Power on mit Attiny:  {power_on}")
    log_schreiben(f"Zeit für Power off mit Attiny: {power_off}")
    set_alarm(power_on, power_off)

    send_lora(f"Zeit für Power on mit Attiny:  {power_on}\nZeit für Power off mit Attiny: {power_off}")
    display_text_and_image("Will-","kommen", Version, "/home/Ento/LepmonOS/startsequenz/Logo_9_9.png",1)
    set_alarm(power_on, power_off)
    try:
        store_times_power(power_on, power_off)
    except Exception as e:
        print(f"Fehler beim Speichern der Zeiten: {e}")
        print("Falle besitzt kein Power Management. Fahre fort")
        
    print("beende Setup")        
