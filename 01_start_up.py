import time
from utils.OLED_panel import display_text

try:
    display_text("Willkommen", "Laden... 2/2", "")
    print("Wilkommen message 2 in Display")
    print("activate virtual environment")
    time.sleep(2)
except Exception as e:
    print(f"Error displaying text on OLED: {e}") 