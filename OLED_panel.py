from PIL import ImageFont, ImageDraw, Image
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import time
import os
from GPIO_Setup import *

oled_font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'FreeSans.ttf'), 14)

# OLED-Setup
Display = i2c(port=1, address=0x3C)
try:
    oled = sh1106(Display)
except:
    pass
oled_font = ImageFont.truetype('FreeSans.ttf', 14)

# Funktion, um Text auf dem OLED anzuzeigen
def display_text(line1, line2, line3, sleeptime =0):
    """
    Zeigt drei Zeilen Text auf dem OLED-Display an.
    Der Text bleibt auf dem Display, bis er überschrieben wird.
    
    :param line1: Text für die erste Zeile
    :param line2: Text für die zweite Zeile
    :param line3: Text für die dritte Zeile
    :param sleeptime: Zeit für displaydauer
    """
    try:
        with canvas(oled) as draw:
            # Hintergrund löschen, um alten Text zu entfernen
            draw.rectangle(oled.bounding_box, outline="black", fill="black")
            # Text in die jeweiligen Zeilen schreiben
            draw.text((3, 5), line1, font=oled_font, fill="white")
            draw.text((3, 25), line2, font=oled_font, fill="white")
            draw.text((3, 45), line3, font=oled_font, fill="white")
        time.sleep(sleeptime) 
    except Exception as e:
        print(f"Error displaying text on OLED: {e}")  
        for _ in range(3):
            turn_on_led("rot")
            time.sleep(0.25)
            turn_off_led("rot")
            time.sleep(0.25)      


def display_text_and_image(line1, line2, line3, image_path,sleeptime =0):
    """
    Zeigt links drei Zeilen Text und rechts ein Bild (64x64 px) auf dem OLED an.
    """
    try:
        logo = Image.open(image_path).convert("1").resize((64, 64))
        with canvas(oled) as draw:
            # Hintergrund löschen
            draw.rectangle(oled.bounding_box, outline="black", fill="black")
            # Bild rechts (z.B. bei 64x128 Display: x=64, y=0)
            draw.bitmap((oled.width - 64, 0), logo, fill=1)
            # Text links (z.B. x=5, y=5/25/45)
            draw.text((3, 5), line1, font=oled_font, fill="white")
            draw.text((3, 25), line2, font=oled_font, fill="white")
            draw.text((3, 45), line3, font=oled_font, fill="white")
            time.sleep(sleeptime)
    except Exception as e:
        print(f"Error displaying text on OLED: {e}")        
        for _ in range(3):
            turn_on_led("rot")
            time.sleep(0.25)
            turn_off_led("rot")
            time.sleep(0.25)        
    
def display_text_with_arrows(line1, line2, line3, sleeptime=0):
    try:
        with canvas(oled) as draw:
            draw.rectangle(oled.bounding_box, outline="black", fill="black")
            draw.text((3, 5), line1, font=oled_font, fill="white")
            draw.text((3, 25), line2, font=oled_font, fill="white")
            draw.text((3, 45), line3, font=oled_font, fill="white")
            draw.text((110, 5), "▲", font=oled_font, fill="white")
            draw.text((110, 25), "→", font=oled_font, fill="white")
            draw.text((110, 45), "▼", font=oled_font, fill="white")
        time.sleep(sleeptime)    
    except Exception as e:
        print(f"Error displaying text on OLED: {e}")
        for _ in range(3):
            turn_on_led("rot")
            time.sleep(0.25)
            turn_off_led("rot")
            time.sleep(0.25)      