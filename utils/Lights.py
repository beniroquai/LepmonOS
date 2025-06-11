import RPi.GPIO as GPIO
import time
from utils.json_read_write import get_value_from_section
from utils.log import log_schreiben

LepiLed_pin = 26
dimmer_pin = 13
Blitz_PMW = 350

GPIO.setmode(GPIO.BCM) # Initialisierung der GPIO und PWM außerhalb der Schleife
GPIO.setup(dimmer_pin, GPIO.OUT)
GPIO.setup(LepiLed_pin, GPIO.OUT)
GPIO.setwarnings(False)

dimmer_pwm = GPIO.PWM(dimmer_pin, Blitz_PMW)
LepiLed_pwm = GPIO.PWM(LepiLed_pin, Blitz_PMW)


def dim_up():
   flash = get_value_from_section("./config/Lepmon_config.json","capture_mode","flash")
   dimmer_pwm.start(0)
   for duty_cycle in range(0, 99,1):
        dimmer_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(flash / 100)
        
      
def dim_down(): 
  flash = get_value_from_section("./config/Lepmon_config.json","capture_mode","flash") 
  dimmer_pwm.start(100)
  for duty_cycle in range(99, 0, -1):
        dimmer_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(flash / 100)
  dimmer_pwm.start(0)



def LepiLED_start():
    flash = get_value_from_section("./config/Lepmon_config.json","capture_mode","flash") 
    LepiLed_pwm.start(0)
    for duty_cycle in range(0, 99, 1):
        LepiLed_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(flash / 100)
        LepiLed_pwm.ChangeDutyCycle(100)
    '''
    LepiLED_message = f"Lepmon#{sensor_id} LepiLED eingeschaltet"
    try:
        uart.write(LepiLED_message.encode('utf-8') + b'\n')
    except Exception as e:
        print(f"Fehler beim Lora senden: {e}")
        pass   
    '''

def LepiLED_ende():
    flash = get_value_from_section("./config/Lepmon_config.json","capture_mode","flash") 
    print("dimme UV LED runter")
    LepiLed_pwm.start(100)
    for duty_cycle in range(99, 0, -1):
        LepiLed_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(flash / 100)
        LepiLed_pwm.ChangeDutyCycle(0)
    LepiLed_pwm.start(0)
