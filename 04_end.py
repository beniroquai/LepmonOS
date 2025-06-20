import os
from utils.lora import send_lora
from utils.OLED_panel import display_text
from utils.end import trap_shutdown
from utils.log import log_schreiben
import time


if __name__ == "__main__":
    try:
        log_schreiben("Shutdown sequence initiated")
        print("Starting enhanced shutdown sequence")
        
        # Use the enhanced shutdown function
        trap_shutdown()
        
    except Exception as e:
        print(f"Enhanced shutdown failed, using fallback: {e}")
        log_schreiben(f"Enhanced shutdown failed: {e}")
        
        # Fallback to basic shutdown
        send_lora("Falle fährt in 1 Minute herunter und startet dann neu. Letzte Nachricht im aktuellen Run\nBeachte, dass der Stromcontroller die Falle ggf. erst später am Tag wieder aktiviert")
        i = 60
        for _ in range(60):
            display_text("Falle startet","neu in",f"{i} Sekunden")
            i -= 1
            time.sleep(1)
            
        os.system("sudo shutdown -r 1")


