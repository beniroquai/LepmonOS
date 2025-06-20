from utils.fram_direct import *
import time
from configparser import ConfigParser
from datetime import datetime, timedelta
import re

CONFIG_PATH = "./config/fram_config.ini"

def write_config_to_fram():
    sn = input("🔢 Seriennummer im Format SN123456: ").strip().upper()
    if not sn.startswith("SN") or not re.match(r"^SN\d{6}$", sn):
        print("❌ Ungültiges Format. Beispiel: SN123456")
        return
    print(f"Seriennummer: {sn}")  
    time.sleep(2)  

    now = datetime.now()
    ts_now = now.strftime("%Y-%m-%d %H:%M:%S")
    ts_plus1h = (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    

    config = ConfigParser()
    config.read(CONFIG_PATH)
    
 ####Attiny Data####       
    write_fram(0x0000, "power_on")
    write_fram(0x0010, ts_now)
    write_fram(0x0030, "power_off")
    write_fram(0x0040, ts_plus1h)
    write_fram(0x0060, "status")
#### Raspi Data ####  
    write_fram(0x0100, "serial_number")
    write_fram(0x0110, sn)
    write_fram(0x0120, "trap_version") 
    write_fram(0x0130, config.get("FRAM", "fallen_version"))    
    write_fram(0x0140, "backplane_vers") 
    write_fram(0x0150, config.get("FRAM", "backplane_version")) 
    write_fram(0x0160, "delivery_PMJ")  
    write_fram(0x0170, config.get("FRAM", "lieferdatum_an_PMJ"))  
#### laufzeit Labels ####
    write_fram(0x0300, "boot_counter")
    write_fram(0x0320, "user_counter")
    write_fram(0x0340, "total_runtime")
    write_fram(0x0360, "last_start")
    write_fram(0x0380, "GB_used_start")
#### Software Informationen ####    
    write_fram(0x0500, "software")
    write_fram(0x0510, config.get("FRAM", "software_date"))
    write_fram(0x0520, config.get("FRAM", "software_version"))

#### Fehlercode 0###
    write_fram(0x0800, "error_code")
    write_fram_bytes(0x081F, (0).to_bytes(4, byteorder='big'))  # Fehlercode 0
#### Fehlerhäufigkeitstabelle ####   
    write_fram(0x0820, "error_counts") 
    write_fram(0x0830, "Err01")
    write_fram(0x0850, "Err02")
    write_fram(0x0870, "Err03") 
    write_fram(0x0890, "Err04")
    write_fram(0x08B0, "Err05")
    write_fram(0x08D0, "Err06")
    write_fram(0x08F0, "Err07")
    write_fram(0x0910, "Err08")
    write_fram(0x0930, "Err09")
    write_fram(0x0950, "Err10")
    write_fram(0x0970, "Err11")
    write_fram(0x0990, "Err12")
    write_fram(0x09B0, "Err13")


    print("Alle Werte erfolgreich in FRAM geschrieben.")

if __name__ == "__main__":
    clear_fram("setup")
    write_config_to_fram()
    dump_fram(0x0000, 0x1FFF)