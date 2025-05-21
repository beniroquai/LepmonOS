FRAM_MEMORY_MAP = {
    (0x0000, 0x001F): {
        "size": 32,
        "description": "Powersave: Timestamp Power ON,      Regime Raspi + ATTINY"
    },
    (0x0020, 0x003F): {
        "size": 32,
        "description": "Powersave: Timestamp, Power OFF,    Regime Raspi + ATTINY"
    },
    (0x0040, 0x004F): {
        "size": 16,
        "description": "Status,                            Regime Raspi + ATTINY"
    },
    (0x0050, 0x00FF): {
        "size": 176,
        "description": "free,                              Regime Raspi + ATTINY"
    }, 
    (0x0100, 0x013F): {
        "size": 64,
        "description": "Software Version,                 Raspi live"
    },
    (0x0140, 0x0141F): {
        "size": 32,
        "description": "Fallen Version,                   Raspi live"
    },
    (0x01420, 0x0142F): {
        "size": 16,
        "description": "Backplane Version,                Raspi live"
    },
    (0x01430, 0x0143F): {
        "size": 16,
        "description": "Lieferdatum an PMJ,              Raspi live"
    },
    (0x01440, 0x1BFF): {
        "size": 1984,
        "description": "free,                            Raspi live"
    },
    (0x1C00, 0x1C0F): {
        "size": 16,
        "description": "Serialnumber,                    Versionen Raspi Fertigung/Prüfung"
    },
    (0x1C10, 0x1C2F): {
        "size": 32,
        "description": "Kalibrierung,                   Versionen Raspi Fertigung/Prüfung"
    },
    (0x1C30, 0x1FFF): {
        "size": 976,
        "description": "free,                           Versionen Raspi Fertigung/Prüfung"
    }
}


def get_memory_section(addr: int):
    for (start, end), info in FRAM_MEMORY_MAP.items():
        if start <= addr <= end:
            return info
    return None