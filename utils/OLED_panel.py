from PIL import ImageFont, ImageDraw, Image
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import time
import os
# Try to load custom font, fallback to default font if not available
try:
    oled_font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'FreeSans.ttf'), 14)
except (OSError, IOError):
    # Fallback to default font if FreeSans.ttf is not found
    try:
        # Try common system fonts
        oled_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except (OSError, IOError):
        # Final fallback to PIL's default font
        oled_font = ImageFont.load_default()

# OLED-Setup
Display = i2c(port=1, address=0x3C)
try:
    oled = sh1106(Display)
except:
    # dummy class for OLED in case it'S not connected
    class ssh1106_:
        def __init__(self, Display):
            pass

        def bounding_box(self):
            return (0, 0, 128, 64)

        def clear(self):
            pass

        def show(self):
            pass

        def text(self, position, text, font, fill):
            pass

        def bitmap(self, position, image, fill):
            pass
        
    oled = ssh1106_(Display)

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
    # Convert image to 1-bit mode
    logo = Image.open(path).convert("1")

    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.bitmap((0, 0), logo, fill="white")