import os
from utils.lora import  send_lora
from utilsOLED_panel import display_text
import time


send_lora("Falle fährt in 1 Minute herunter und startet dann neu. Letzte Nachricht im aktuellen Run\nBeachte, dass der Stromcontroller die Falle ggf. erst später am Tag wieder aktiviert")
i = 60
for _ in range(60):
    display_text("Falle startet","neu in",f"{i} Sekunden")
    i -= 1
    time.sleep(1)
    
os. system("sudo shutdown -r 1")


