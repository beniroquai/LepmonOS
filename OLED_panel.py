from PIL import ImageFont, ImageDraw, Image
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import time
import os
oled_font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'FreeSans.ttf'), 14)

# OLED-Setup
Display = i2c(port=1, address=0x3C)
oled = sh1106(Display)
oled_font = ImageFont.truetype('FreeSans.ttf', 14)

# Funktion, um Text auf dem OLED anzuzeigen
def display_text(line1, line2, line3):
    """
    Zeigt drei Zeilen Text auf dem OLED-Display an.
    Der Text bleibt auf dem Display, bis er überschrieben wird.
    
    :param line1: Text für die erste Zeile
    :param line2: Text für die zweite Zeile
    :param line3: Text für die dritte Zeile
    """
    with canvas(oled) as draw:
        # Hintergrund löschen, um alten Text zu entfernen
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        # Text in die jeweiligen Zeilen schreiben
        draw.text((5, 5), line1, font=oled_font, fill="white")
        draw.text((5, 25), line2, font=oled_font, fill="white")
        draw.text((5, 45), line3, font=oled_font, fill="white")





def display_image (path):
    """
    Zeigt ein Bild auf dem OLED-Display an.
    
    :param path: Pfad zum Bild
    """
    logo = Image.open(path)  # Konvertiere das Bild in Schwarz-Weiß

    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.bitmap((0, 0), logo, fill="white") 