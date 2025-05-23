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


if __name__ == "__main__":
    dim_down()
    RPI_time()
    Version = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "version")
    date = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "date") 

    try:
        display_text("Willkommen", "Laden... 1/10", f"{Version}")
        print("Wilkommen message 1 in Display")
        time.sleep(3)
    except Exception as e:
        print(f"Error displaying text on OLED: {e}")
        print("Display not working")    

    ram_counter(0x01F0)
    set_serial_number()
    delete_error_code()


    display_text("Willkommen", "Laden... 2/10", f"{Version}")
        

    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_folder", "")
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_log", "")
    print("Konfigurationsdatei zurückgesetzt")
    

    time.sleep(1)
    display_text("Willkommen", "Laden... 3/10", f"{Version}")
    time.sleep(1)
    display_text("Willkommen", "Laden... 4/10", f"{Version}")   
    time.sleep(1)
    display_text("Willkommen", "Laden... 5/10", f"{Version}")     
    time.sleep(1)
    display_text("Willkommen", "Laden... 6/10", f"{Version}")  
    time.sleep(1)
    display_text("Willkommen", "Laden... 7/10", f"{Version}")      
    erstelle_ordner()
    initialisiere_logfile()
    log_schreiben(f"Software- Version: {Version} vom {date}")
    log_schreiben("Experiment Parameter:")

    display_text("Willkommen", "Laden... 8/10", f"{Version}")  
    send_lora("Berechne Zeiten für Power Managament")
    sunset, sunrise, Zeitzone = get_sun()

    log_schreiben(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}")
    log_schreiben(f"Sonnenaufgang:   {sunrise.strftime('%H:%M:%S')}")

    send_lora(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}\nSonnenaufgang: {sunrise.strftime('%H:%M:%S')}")
    
    display_text("Willkommen", "Laden... 9/10", f"{Version}") 
    power_on, power_off = get_times_power()

    print("power on time:",  power_on)
    print("power off time:", power_off)
    log_schreiben(f"Zeit für Power on mit Attiny:  {power_on}")
    log_schreiben(f"Zeit für Power off mit Attiny: {power_off}")
    set_alarm(power_on, power_off)

    send_lora(f"Zeit für Power on mit Attiny:  {power_on}\nZeit für Power off mit Attiny: {power_off}")

    set_alarm(power_on, power_off)
    store_times_power(power_on, power_off)
    display_text("Willkommen", "Laden... 10/10", f"{Version}")  