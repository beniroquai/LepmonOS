FRAM_MEMORY_MAP = {
    (0x0000, 0x000F): {
        "size": 16,
        "description": "Text: Start_label"
    },    
    (0x0010, 0x002F): {
        "size": 32,
        "description": "Powersave: Timestamp Power ON,              Regime Raspi + ATTINY"
    },
    (0x0030, 0x003F): {
        "size": 16,
        "description": "Text: End_label"
    },        
    (0x0040, 0x005F): {
        "size": 32,
        "description": "Powersave: Timestamp, Power OFF,            Regime Raspi + ATTINY"
    },
    (0x0060, 0x006F): {
        "size": 16,
        "description": "Status_Label"
    },
    (0x0070, 0x007F): {
        "size": 16,
        "description": "Statusplatzhalter,                          Regime Raspi + ATTINY"
    },    
    (0x0070, 0x00FF): {
        "size": 144,
        "description": "free,                                       Regime Raspi + ATTINY"
    }, 
    (0x0100, 0x010F): {
        "size": 16,
        "description": "Serialnumber_label"
    },
    (0x0110, 0x011F): {
        "size": 16,
        "description": "Serialnumber"
    },   
    (0x0120, 0x012F): {
        "size": 16,
        "description": "Software_Version_Label"
    },    
    (0x0130, 0x017F): {
        "size": 64,
        "description": "verwendete_Software_Version"
    },
    (0x0180, 0x018F): {
        "size": 16,
        "description": "Fallen_Version_Label"
    },
    (0x0190, 0x019F): {
        "size": 16,
        "description": "Fallen_Generation"
    },
    (0x01A0, 0x01AF): {
        "size": 16,
        "description": "Backplane_Version_Label"
    },
    (0x01B0, 0x01BF): {
        "size": 16,
        "description": "Platinen Version"
    },    
    (0x01C0, 0x01CF): {
        "size": 16,
        "description": "Lieferdatum_an_PMJ_Label"
    },
    (0x01D0, 0x01DF): {
        "size": 16,
        "description": "Lieferdatum_an_PMJ"
    },    
    (0x01E0, 0x01EF): {
        "size": 16,
        "description": "Anschalt_counter_Label"
    },
    (0x01F0, 0x01FF): {
        "size": 16,
        "description": "Anschalt_counter"
    },    
    (0x0200, 0x0FFFF): {
        "size": 6,
        "description": "free"
    },        
    
    (0x1000, 0x100F): {
        "size": 16,
        "description": "Fehler"
    },    
    (0x1010, 0x101F): {
        "size": 16,
        "description": "Fehlercode"
    },        
    (0x1020, 0x10F0): {
        "size": 224,
        "description": "Fehlerfrequenz"
    },
    (0x1020, 0x01DF): {
        "size": 1,
        "description": "free"
    },    
    (0x1C00, 0x1FFF): {
        "size": 1024,
        "description": "free"
    }
}


def get_memory_section(addr: int):
    for (start, end), info in FRAM_MEMORY_MAP.items():
        if start <= addr <= end:
            return info
    return None