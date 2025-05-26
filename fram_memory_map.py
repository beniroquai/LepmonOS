from tabulate import tabulate

FRAM_MEMORY_MAP = {
#### Attiny Data####    
    (0x0000, 0x000F): {
        "size": 16,
        "description": "Power_ON_Timestamp_Label,                               Label"
    },    
    (0x0010, 0x002F): {
        "size": 32,
        "description": "Power_ON_Timestamp,                                     Regime Raspi + ATTINY"
    },
    (0x0030, 0x003F): {
        "size": 16,
        "description": "Power_OFF_Timestamp_label                               Label"  
    },        
    (0x0040, 0x005F): {
        "size": 32,
        "description": "Power_OFF_Timestamp,                                    Regime Raspi + ATTINY"
    },
    (0x0060, 0x006F): {
        "size": 16,
        "description": "Status_Label                                            Label"
    },
    (0x0070, 0x007F): {
        "size": 16,
        "description": "Statusplatzhalter,                                      Regime Raspi + ATTINY"
    },    
    (0x0070, 0x00FF): {
        "size": 144,
       
        "description": "free"
    }, 
#### Raspi Data ####
####Setup Prozess####    
    (0x0100, 0x010F): {
        "size": 16,
        "description": "Serialnumber_label                                      Label"
    },
    (0x0110, 0x011F): {
        "size": 16,
        "description": "Serialnumber_value                                      Setup Prozess"
    },      
    (0x0120, 0x012F): {
        "size": 16,
        "description": "Fallen_Version_Label                                    Label"
    },
    (0x0130, 0x013F): {
        "size": 16,
        "description": "Fallen_Version_Value                                    Setup Prozess"
    }, 
    (0x0140, 0x014F): {
        "size": 16,
        "description": "Backplane_Version_Label                                 Label"
    },         
   (0x0150, 0x015F): {
        "size": 16,
        "description": "Backplane_Version_Value                                 Setup Prozess"
    },
    (0x0160, 0x016F): {
        "size": 16,
        "description": "Lieferdatum_an_PMJ_Label                                Label"
    },
    (0x0170, 0x017F): {
        "size": 16,
        "description": "Lieferdatum_an_PMJ_Date                                 Setup Prozess"
    },       
#### Laufzeit Daten ####
    (0x0300, 0x030E): {
        "size": 16,
        "description": "Boot_counter_Label                                      Label"
    },    
    (0x0310, 0x031F): {
        "size": 16,
        "description": "Boot_counter_Value                                      RPI"
    },  
    (0x0320, 0x032F): {
        "size": 15,
        "description": "User_Interface_counter_Label                            Label"
    },
    (0x0330, 0x033F): {
        "size": 16,
        "description": "User_Interface_counter_Value                            RPI"
    },  
    (0x0340, 0x034E): {
        "size": 16,
        "description": "total_runtime_label                                    Label"
    },           
    (0x0350, 0x035F): {
        "size": 16,
        "description": "runtime                                                 RPI"
    },  
    (0x0360, 0x036F): {
        "size": 16,
        "description": "timestamp_last_start_Label                              Label"
    },       
    (0x0370, 0x037F): {
        "size": 16,
        "description": "timestamp_last_start                                    RPI"
    }, 
     (0x0380, 0x038F): {
        "size": 16,
        "description": "Gigabytes_free_at_start_label                           Label"
    },      
     (0x0390, 0x039F): {
        "size": 16,
        "description": "Gigabytes_free_at_start_Value                           RPI"
    },         
     (0x03A0, 0x04FF): {
        "size": 384,
        "description": "free"
    },                               
#### Software Version ####
    (0x0500, 0x050F): {
        "size": 16,
        "description": "Software_Information_Label                              Label"
    },
    (0x0510, 0x051F): {
        "size": 16,
        "description": "Software_Date                                           RPI"
    },  
    (0x0520, 0x055F): {
        "size": 64,
        "description": "Software_Version                                        RPI"
    },  
    (0x0560, 0x07FF): {
        "size": 672,
        "description": "free"
    },        

    (0x0800, 0x080F): {
        "size": 16,
        "description": "aktueller_Fehler_Label                                  Label"
    },
    (0x0810, 0x081F): {
        "size": 16,
        "description": "aktueller_Fehler_Code                                   RPI"
    },      
    (0x0820, 0x082F): {
        "size": 16,
        "description": "Fehlerfrequenz_Tabelle_header                           Tabelle"
    },
      (0x0830, 0x083F): {
        "size": 16, 
        "description": "Err  1 Kamera -  Häufigkeit_Label                       Label"
    },
    (0x0840, 0x084F): {
        "size": 16,
        "description": "Err  1 Kamera -  Häufigkeit_Value                       RPI"   
    },     
    (0x0850, 0x085F): {
        "size": 16,
        "description": "Err  2 Fokus -  Häufigkeit_Label                        Label"
    },
    (0x0860, 0x086F): {
        "size": 16,
        "description": "Err  2 Fokus -  Häufigkeit_Value                        RPI"
    },    
    (0x0870, 0x087F): {
        "size": 16,
        "description": "Err  3 USB -  Häufigkeit_Label                          Label"
    },
    (0x0880, 0x088F): {
        "size": 16,
        "description": "Err  3 USB -  Häufigkeit_Value                          RPI"
    },    
    (0x0890, 0x089F): {
        "size": 16,
        "description": "Err  4 Lichtsensor -  Häufigkeit_Label                  Label"
    },
    (0x08A0, 0x08AF): {
        "size": 16,
        "description": "Err  4 Lichtsensor -  Häufigkeit_Value                  RPI" 
    },
    (0x08B0, 0x08BF): {
        "size": 16,
        "description": "Err  5 Umweltsensor -  Häufigkeit_Label                 Label"
    },
    (0x08C0, 0x08CF): {
        "size": 16,
        "description": "Err  5 Umweltsensor -  Häufigkeit_Value                 RPI"
    },
    (0x08D0, 0x08DF): {
        "size": 16,
        "description": "Err  6 Innen-Temperatur -  Häufigkeit_Label             Label"
    },
    (0x08E0, 0x08EF): {
        "size": 16,
        "description": "Err  6 Innen-Temperatur -  Häufigkeit_Value             RPI"
    },
    (0x08F0, 0x08FF): {
        "size": 16,
        "description": "Err  7 Stromsensor -  Häufigkeit_Label                  Label"
    },
    (0x0900, 0x090F): {
        "size": 16,
        "description": "Err  7 Stromsensor -  Häufigkeit_Value                  RPI"
    },
    (0x0910, 0x091F): {
        "size": 16,
        "description": "Err  8 Hardware Uhr -  Häufigkeit_Label                 Label"
    },
    (0x0920, 0x092F): {
        "size": 16,
        "description": "Err  8 Hardware Uhr -  Häufigkeit_Value                 RPI"
    },
    (0x0930, 0x093F): {
        "size": 16,
        "description": "Err  9 FRAM -  Häufigkeit_Label                         Label"
    },
    (0x0940, 0x094F): {
        "size": 16,
        "description": "Err  9 FRAM -  Häufigkeit_Value                         RPI"
    },
    (0x0950, 0x095F): {
        "size": 16,
        "description": "Err 10 Logging -  Häufigkeit_Label                      Label"
    },
    (0x0960, 0x096F): {
        "size": 16,
        "description": "Err 10 Logging -  Häufigkeit_Value                      RPI"
    },
    (0x0970, 0x097F): {
        "size": 16,
        "description": "Err 11 Checksumme - Häufigkeit_Label                    Label"
    },
    (0x0980, 0x098F): {
        "size": 16,
        "description": "Err 11 Checksumme - Häufigkeit_Value                    RPI"
    },
    (0x0990, 0x099F): {
        "size": 16,
        "description": "Err12 Beleuchtungs LED - Häufigkeit_Label               Label"
    },
    (0x09A0, 0x09AF): {
        "size": 16,
        "description": "Err12 Beleuchtungs LED - Häufigkeit_Value               RPI"
    },
    (0x09B0, 0x09BF): {
        "size": 16,
        "description": "Err13 Metadaten Tabelle - Häufigkeit_Label              Label"
    },
    (0x09C0, 0x09CF): {
        "size": 16,
        "description": "Err13 Metadaten Tabelle - Häufigkeit_Value              RPI"
    },
    (0x09D0, 0x10BF): {
        "size": 1776,
        "description": "free"
    },    
    (0x10C0, 0x1FFF): {
        "size": 1024,
        "description": "free                               Produktion"
    }
}

def print_fram_memory_map_tab():
    table = []
    for (start, end), info in FRAM_MEMORY_MAP.items():
        table.append([f"0x{start:04X}", f"0x{end:04X}", info['size'], info['description']])
    print(tabulate(table, headers=["Start", "Ende", "Größe", "Beschreibung"], tablefmt="github"))


    
    
if __name__ == "__main__":

    print_fram_memory_map_tab()