from utils.times import get_times_power
from utils.OLED_panel import display_text, display_image
from utils.service import *
from utils.log import log_schreiben
from utils.lora import send_lora
from utils.error_handling import *
from utils.times import *
from utils.json_read_write import *
from utils.Lights import dim_down
from utils.RTC_alarm import set_alarm
from utils.fram_operations import *
from utils.runtime import on_start
from utils.GPIO_Setup import turn_off_led
from utils.end import trap_shutdown
try:
    from utils.FRAM_acess import *
except Exception as e:
     error_message(9,e)

import time


if __name__ == "__main__":
    # Initialize startup sequence
    dim_down()
    turn_off_led("blau")
    print("starte Setup")      
    # RPI_time()
    on_start()
    
    # Display manual link image
    try:
        display_image("./startsequence/link_manual.png")
        time.sleep(8)
    except Exception as e:
        print(f"Could not display manual link: {e}")
        display_text("Beachte", "Anleitung", "")
        time.sleep(3)
    
    # Get version information
    try:
        Version = get_value_from_section("./config/Lepmon_config.json", "software", "version")
        date = get_value_from_section("./config/Lepmon_config.json", "software", "date") 
    except Exception as e:
        Version = "V1.0"
        date = "2024"
        print(f"Could not read version info: {e}")
    
    # Logo startup sequence
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))    
        for i in range(1, 10):
            display_image(os.path.join(current_dir,f"startsequence/Logo_{i}_9.png"))
            time.sleep(1)
        print("Logo sequence completed")
    except Exception as e:
        print(f"Logo sequence failed: {e}")
        display_text("Willkommen", f"Version {Version}", "")
        time.sleep(3)

    # Read serial number from FRAM with fallback to JSON
    sn = None
    attempts = 0
    max_attempts = 5
    
    while sn == None and attempts < max_attempts:
        try:
            time.sleep(2)
            sn = read_fram(0x0110, 8).strip()
            if sn and sn != "":
                print(f"Serial Number from FRAM: {sn}")
                break
        except Exception as e:
            print(f"FRAM read attempt {attempts + 1} failed: {e}")
        
        try:
            sn = get_value_from_section("./config/LepmonOS_serial_number.json", "general", "serielnumber")
            if sn and sn != "":
                print(f"Serial Number from JSON: {sn}")
                break
        except Exception as e:
            print(f"JSON read attempt {attempts + 1} failed: {e}")
        
        attempts += 1
        time.sleep(1)
    
    if sn == None:
        sn = "UNKNOWN"
        print("Could not read serial number, using default")
        
    # Write serial number to config
    try:
        write_value_to_section("./config/Lepmon_config.json", "general", "serielnumber", sn)
    except Exception as e:
        print(f"Could not write serial number to config: {e}")

    # Send startup message
    try:
        send_lora("Starte Lepmon Software")
        print("Lora startup message sent")
    except Exception as e:
        print(f"Lora not available: {e}")

    # Initialize system components
    try:
        erstelle_ordner()
        initialisiere_logfile()
        log_schreiben("Startup: System initialization completed")
    except Exception as e:
        print(f"System initialization error: {e}")

    # Calculate and display sun times
    try:
        sunset, sunrise, Zeitzone = get_sun()
        print(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}")
        print(f"Sonnenaufgang: {sunrise.strftime('%H:%M:%S')}")
        
        log_schreiben(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}")
        log_schreiben(f"Sonnenaufgang:   {sunrise.strftime('%H:%M:%S')}")
        send_lora(f"Sonnenuntergang: {sunset.strftime('%H:%M:%S')}\nSonnenaufgang: {sunrise.strftime('%H:%M:%S')}")
    except Exception as e:
        error_message(12, f"Sun time calculation error: {e}")

    # Calculate and write power times
    try:
        power_on, power_off = get_times_power()
        print("power on time:",  power_on)
        print("power off time:", power_off)
        log_schreiben(f"Zeit für Power on mit Attiny:  {power_on}")
        log_schreiben(f"Zeit für Power off mit Attiny: {power_off}")
        send_lora(f"Zeit für Power on mit Attiny:  {power_on}\nZeit für Power off mit Attiny: {power_off}")
        
        # Write times to FRAM
        write_fram(8, str(power_on))
        write_fram(17, str(power_off))
        time.sleep(1)
        print("start time and stop time written to FRAM")
        log_schreiben("Start & Stop Zeiten im FRam aktualisiert")
        
    except Exception as e:
        error_message(9,"Fehler in der Kommunikation zwischen Raspberry Pi und Fram Modul. Zeiten für An und Ausschalten der Falle nicht aktualisiert.")
        time.sleep(5)

    print("Startup sequence completed successfully")