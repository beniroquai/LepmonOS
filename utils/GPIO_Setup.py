import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

# Definiere die Pin-Nummern für LEDs und Knöpfe
LED_PINS = {
    'gelb': 22,    # GPIO 17 für gelbe LED
    'blau': 6,    # GPIO 27 für blaue LED
    'rot': 17      # GPIO 22 für rote LED
}

BUTTON_PINS = {
    'oben': 23,     # GPIO 5 für Knopf oben
    'unten': 24,    # GPIO 6 für Knopf unten
    'rechts': 8,  # GPIO 13 für Knopf rechts
    'enter': 7    # GPIO 19 für Knopf enter
}

# Setup der GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LEDs als Ausgang und Knöpfe als Eingang setzen
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # LEDs aus zu Beginn

for pin in BUTTON_PINS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Knöpfe als Eingänge mit Pull-up-Widerstand

# PWM für LEDs einrichten
led_pwm = {}
for color, pin in LED_PINS.items():
    pwm = GPIO.PWM(pin, 1000)  # PWM bei 1kHz
    pwm.start(0)  # Startwert 0 (LEDs aus)
    led_pwm[color] = pwm

# Funktion, um die Helligkeit der LEDs zu ändern (Dimmung)
def dim_led(color, brightness):
    """Dimmt die angegebene LED (z.B. 'gelb', 'blau', 'rot')."""
    if color in led_pwm:
        led_pwm[color].ChangeDutyCycle(brightness)  # Helligkeit zwischen 0 und 100

# Funktion, um den Status eines Knopfs abzufragen
def button_pressed(button_name):
    """
    Überprüft, ob der angegebene Knopf gedrückt wurde.

    :param button_name: Name des Knopfes ('oben', 'unten', 'rechts', 'enter').
    :return: True, wenn der Knopf gedrückt wurde, sonst False.
    :raises ValueError: Wenn der angegebene Knopfname nicht existiert.
    """
    if button_name not in BUTTON_PINS:
        available_buttons = ", ".join(BUTTON_PINS.keys())
        raise ValueError(f"Ungültiger Knopfname '{button_name}'. Verfügbare Knöpfe: {available_buttons}")
    
    return GPIO.input(BUTTON_PINS[button_name]) == GPIO.LOW  # Knopf gedrückt: LOW

# Beispiel-Funktionen, die in anderen Skripten aufgerufen werden können
def turn_on_led(color):
    """Schaltet die angegebene LED ein (volle Helligkeit)."""
    dim_led(color, 100)

def turn_off_led(color):
    """Schaltet die angegebene LED aus."""
    dim_led(color, 0)


if __name__ == "__main__":
    print("Teste GPIO-Setup...")
    turn_on_led("blau")
    turn_off_led("blau")    