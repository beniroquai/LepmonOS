from times import get_times_power
from OLED_panel import display_text
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



if __name__ == "__main__":
    dim_down()
    RPI_time()
    on_start()
    Version = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "version")
    date = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "date") 
    sn = read_fram(0x0110, 8).strip()
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "serielnumber", sn)

    send_lora("Starte Lepmon Software")
    
    try:
        display_text("Willkommen", "Laden... 1/9", f"{Version}")
        print("Wilkommen message 1 in Display")
        time.sleep(3)
    except Exception as e:
        print(f"Error displaying text on OLED: {e}")
        print("Display not working")    

    ram_counter(0x0310)
    
    set_serial_number()
    delete_error_code()


    display_text("Willkommen", "Laden... 2/9", f"{Version}")
        

    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_folder", "")
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_log", "")
    print("Konfigurationsdatei zurückgesetzt")
    

    time.sleep(1)
    display_text("Willkommen", "Laden... 3/9", f"{Version}")
    time.sleep(1)
    display_text("Willkommen", "Laden... 4/9", f"{Version}")   
    time.sleep(1)
    display_text("Willkommen", "Laden... 5/9", f"{Version}")     
    time.sleep(1)
    display_text("Willkommen", "Laden... 6/9", f"{Version}")  
    time.sleep(1)
    display_text("Willkommen", "Laden... 7/9", f"{Version}")      
    erstelle_ordner()
    initialisiere_logfile()
    log_schreiben(f"Software- Version: {Version} vom {date}")
    log_schreiben("Experiment Parameter:")

    display_text("Willkommen", "Laden... 8/9", f"{Version}")  
    send_lora("Berechne Zeiten für Power Managament")
    sunset, sunrise, Zeitzone = get_sun()

    log_schreiben(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}")
    log_schreiben(f"Sonnenaufgang:   {sunrise.strftime('%H:%M:%S')}")

    send_lora(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}\nSonnenaufgang: {sunrise.strftime('%H:%M:%S')}")
    
    power_on, power_off = get_times_power()

    log_schreiben(f"Zeit für Power on mit Attiny:  {power_on}")
    log_schreiben(f"Zeit für Power off mit Attiny: {power_off}")
    set_alarm(power_on, power_off)

    send_lora(f"Zeit für Power on mit Attiny:  {power_on}\nZeit für Power off mit Attiny: {power_off}")

    set_alarm(power_on, power_off)
    store_times_power(power_on, power_off)
    display_text("Willkommen", "Laden... 9/9", f"{Version}")  