from times import get_times_power
from OLED_panel import display_text
from service import *
from log import log_schreiben
from lora import send_lora
from error_handling import *
import time
from times import *
from json_read_write import write_value_to_section
from Lights import dim_down

try:
    from fram_direct import *
    SN = read_fram(0x0110, 8)
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "serielnumber", SN)
    print("Seriennummer in config geschrieben")
except Exception as e:
     error_message(9,e)

dim_down()

write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "errorcode", "0")
try:
    write_fram(0x1010,"0")  
    write_fram(0x1011,"0")    
    write_fram(0x1012,"0") 
    write_fram(0x1013,"0") 
    print("Fehlercode in FRAM auf 0 gesetzt")
except Exception as e:
    error_message(9,e)
    print("Fehlercode in FRAM nicht gelöscht")
     
     
try:
    display_text("Willkommen", "Laden... 1/2", "")
    print("Wilkommen message 1 in Display")
    time.sleep(3)
except Exception as e:
    print(f"Error displaying text on OLED: {e}")
    print("Display not working")
    
send_lora("Starte Falle\nBerechne Zeiten für FRam")

write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_folder", "")
write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_log", "")
print("Konfigurationsdatei zurückgesetzt")
time.sleep(6)

erstelle_ordner()
initialisiere_logfile()

log_schreiben("Experiment Parameter:")

sunset, sunrise, Zeitzone = get_sun()
print(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}")
print(f"Sonnenaufgang: {sunrise.strftime('%H:%M:%S')}")

log_schreiben(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}")
log_schreiben(f"Sonnenaufgang:   {sunrise.strftime('%H:%M:%S')}")

send_lora(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}\nSonnenaufgang: {sunrise.strftime('%H:%M:%S')}")
   

power_on, power_off = get_times_power()


print("power on time:",  power_on)
print("power off time:", power_off)
log_schreiben(f"Zeit für Power on mit Attiny:  {power_on}")
log_schreiben(f"Zeit für Power off mit Attiny: {power_off}")

send_lora(f"Zeit für Power on mit Attiny:  {power_on}\nZeit für Power off mit Attiny: {power_off}")
  

try:
    write_fram(0x0010, str(power_on))
    write_fram(0x0040, str(power_off))
    time.sleep(1)
    print("start time and stop time written to FRAM")
    log_schreiben("Start & Stop Zeiten im FRam aktualisiert")

except Exception as e:
    error_message(9,"Fehler in der Kommunikation zwischen Raspberry Pi und Fram Modul. Zeiten für An und Ausschalten der Falle nicht aktualisiert.")
    time.sleep(5)