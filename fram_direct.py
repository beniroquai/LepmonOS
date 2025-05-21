import smbus2
import time
from fram_memory_map import FRAM_MEMORY_MAP, get_memory_section  # Import der Map & Funktion

I2C_BUS = 1
FRAM_ADDRESS = 0x50  # I2C-Adresse des FM24CL64B
bus = smbus2.SMBus(I2C_BUS)


def write_fram(address: int, text: str):
    """
    Schreibt einen String byteweise an eine Adresse (max 64 kB FRAM).

    📚 Speicherstruktur (Adressbereiche, Nutzung):
    ┌────────────┬─────┬──────────────────────────────────────────────────────┐
    │ Bereich    │ Gr. │ Beschreibung                                         │
    ├────────────┼─────┼──────────────────────────────────────────────────────┤
    │ 0x0000-00FF│ 256 │ Powersave: Timestamps, Status, Regime Raspi/ATtiny   │
    │ 0x0100-0BFF│6912 │ Laufzeitdaten & Logging Raspi                        │
    │ 0x1C00-1FFF│1024 │ Seriennummer, Kalibrierung, Versionen, Produktion    │
    └────────────┴─────┴──────────────────────────────────────────────────────┘
    """
    data = text.encode("utf-8")
    for offset, byte in enumerate(data):
        high = ((address + offset) >> 8) & 0xFF
        low = (address + offset) & 0xFF
        bus.write_i2c_block_data(FRAM_ADDRESS, high, [low, byte])
    print(f" '{text}' geschrieben an 0x{address:04X}")

def read_fram(address: int, length: int) -> str:
    """Liest eine feste Anzahl Bytes ab Adresse und gibt als String zurück."""
    result = bytearray()
    for offset in range(length):
        high = ((address + offset) >> 8) & 0xFF
        low = (address + offset) & 0xFF
        bus.write_i2c_block_data(FRAM_ADDRESS, high, [low])
        byte = bus.read_byte(FRAM_ADDRESS)
        result.append(byte)
    decoded = result.decode(errors="ignore").strip()
    print(f"Gelesen von 0x{address:04X} (Länge {length}): '{decoded}'")
    return decoded

def dump_fram(start=0x00, length=0x80):
    """Hexdump des FRAM von Startadresse für gegebene Länge."""
    print("\n Speicher-Dump:")
    for i in range(start, start + length, 16):
        hex_line = ""
        ascii_line = ""
        for j in range(16):
            addr = i + j
            high = (addr >> 8) & 0xFF
            low = addr & 0xFF
            try:
                bus.write_i2c_block_data(FRAM_ADDRESS, high, [low])
                val = bus.read_byte(FRAM_ADDRESS)
            except OSError:
                val = 0x00
            hex_line += f"{val:02X} "
            ascii_line += chr(val) if 32 <= val <= 126 else "."
        print(f"{i:04X}: {hex_line:<48} {ascii_line}")


if __name__ == "__main__":
    print("FRAM-Dump:")

    dump_fram(0x0000, 0x1FFF)