import board
import busio
import adafruit_fram
import time

# I2C initialisieren
i2c = busio.I2C(board.SCL, board.SDA)
fram = adafruit_fram.FRAM_I2C(i2c)

# Funktion zum Schreiben eines Strings an eine Startadresse
def write_fram(start_addr: int, data: str):
        data_bytes = data.encode()
        for i in range(len(data_bytes)):
            fram[start_addr + i] = data_bytes[i]
        print(f"{data} an Adresse {start_addr} geschrieben.")

# Funktion zum Lesen eines Strings ab Startadresse mit fester Länge
def read_fram(start_addr: int, length: int) -> str:
        result = bytearray()
        for i in range(start_addr, start_addr + length):
            value = fram[i]
            if isinstance(value, (bytes, bytearray)):
                result.append(value[0])
            else:
                result.append(value)
        decoded = result.decode().strip()
        print(f"Adresse {start_addr}, Länge {length}: '{decoded}'")
        return decoded
        
if __name__ == "__main__":
    write_fram(128, str(""))
    print("wrote an empty bit on position 128 at FRam")