import serial
from utils.json_read_write import get_value_from_section, get_config_path

try:
    uart = serial.Serial("/dev/serial0", 9600, timeout=1)
except Exception as e:
    print(f"Warnung: Lora Sender nicht initialisiert: {e}")
    pass

def send_lora(main_message):
    try:
        sensor_id = get_value_from_section(get_config_path("Lepmon_config.json"),"general","serielnumber")
        message = f"{sensor_id} start of message\n{main_message}\n{sensor_id} end of message"
    except Exception as e:
        print("Fehler im senden der Nachricht")
    try:
        uart.write(message.encode('utf-8') + b'\n') 
        print(message)
    except Exception as e:
        print("Statusmeldung nicht mit LoraWan gesendet")    


if __name__ == "__main__":
    send_lora()        
