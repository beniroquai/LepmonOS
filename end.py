import os
from lora import  send_lora
from OLED_panel import display_text
import time
from datetime import datetime, timedelta
from times import Zeit_aktualisieren
from RTC_alarm import set_alarm
from json_read_write import  get_value_from_section
try:
    from fram_direct import *
except ImportError:
    print("FRAM module not found. Skipping FRAM related operations.")
    pass

Errorcode = 0
try:
    Errorcode = int(read_fram(0x1010, 3))
except Exception as e:  
    Errorcode = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "errorcode")
    pass
print(f"Fehlercode: {Errorcode}")


if Errorcode >0:
    
    jetzt_local,_ = Zeit_aktualisieren()
    
    jetzt_local_dt = datetime.strptime(jetzt_local, "%Y-%m-%d %H:%M:%S")
    print(f"Aktuelle Zeit: {jetzt_local}")
    Nächstes_Anschalten = jetzt_local_dt + timedelta(minutes=2)
    Nächster_Tag = jetzt_local_dt + timedelta(days=1)
    set_alarm(Nächstes_Anschalten.strftime("%Y-%m-%d %H:%M:%S"), Nächster_Tag.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"Alarm gesetzt auf: {Nächstes_Anschalten.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Alarm gesetzt auf: {Nächster_Tag.strftime('%Y-%m-%d %H:%M:%S')}")
    send_lora(f"Falle fährt in 1 Minuten herunter und startet dann neu. Letzte Nachricht im aktuellen Run\nDie Falle wird in 2 Minuten wieder aktiviert")
    for i in range(60, 0, -1):
        display_text("Falle startet","neu in",f"{i} Sekunden")
        i -= 1
        time.sleep(1)
    
    #os. system("sudo shutdown -r 1")
    os.system("sudo reboot")
    

send_lora("Falle fährt in 1 Minute herunter und startet dann neu. Letzte Nachricht im aktuellen Run\nBeachte, dass der Stromcontroller die Falle ggf. erst später am Tag wieder aktiviert")
i = 60
for _ in range(60):
    display_text("Falle startet","neu in",f"{i} Sekunden")
    i -= 1
    time.sleep(1)
    
#os. system("sudo shutdown -r 1")
os.system("sudo reboot")