import os
from utils.lora import  send_lora
from utils.OLED_panel import display_text
import time
from datetime import datetime, timedelta
from utils.times import Zeit_aktualisieren
from utils.RTC_alarm import set_alarm
from utils.json_read_write import  get_value_from_section
from utils.runtime import on_shutdown
try:
    from utils.fram_direct import *
except ImportError:
    print("FRAM module not found. Skipping FRAM related operations.")
    pass

def trap_shutdown(i):
    try:
        Errorcode = int.from_bytes(read_fram_bytes(0x0810, 4), byteorder='big')
    except Exception as e:  
        try:
            Errorcode = int(get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "errorcode"))
        except Exception:
            Errorcode = 0
    print(f"Fehlercode: {Errorcode}")
    
    if Errorcode > 0:
        jetzt_local, _,_ = Zeit_aktualisieren()
        jetzt_local_dt = datetime.strptime(jetzt_local, "%Y-%m-%d %H:%M:%S")
        print(f"Aktuelle Zeit: {jetzt_local}")
        
        Nächstes_Anschalten = jetzt_local_dt + timedelta(minutes=2)
        Nächster_Tag = jetzt_local_dt + timedelta(days=1)
        set_alarm(Nächstes_Anschalten.strftime("%Y-%m-%d %H:%M:%S"), Nächster_Tag.strftime("%Y-%m-%d %H:%M:%S"))
        print(f"Alarm gesetzt auf: {Nächstes_Anschalten.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Alarm gesetzt auf: {Nächster_Tag.strftime('%Y-%m-%d %H:%M:%S')}")
        send_lora(f"Falle fährt in {i} Sekunden herunter und startet dann neu. Letzte Nachricht im aktuellen Run\nDie Falle wird in 2 Minuten wieder aktiviert")

    if Errorcode == 0:
        send_lora(f"Falle fährt in {i} Sekunden herunter. Letzte Nachricht im aktuellen Run\nBeachte, dass der Stromcontroller die Falle erst kurz vor der nächsten Dämmerung wieder aktiviert")

    for sec in range(i, 0, -1):
        display_text("Falle startet", "neu in", f"{sec} Sekunden",1)
    display_text("", "", "")    
    
    on_shutdown()
    time.sleep(2)
    os.system("sudo reboot")
    display_text("","","")
    #os. system("sudo shutdown -r 1")
    
if __name__ == "__main__":
    trap_shutdown(60)    