from json_read_write import *
from error_handling import error_message
from log import log_schreiben
try:
    from fram_direct import *
except Exception as e:
     print(f"Fehler beim Importieren von fram_direct: {e}")  
     
     
def Power_on_counter():
    """
    Liest eine 4-Byte-Zahl aus dem FRAM, erhöht sie um 1 und schreibt sie zurück.
    Gibt den Wert als vierstelligen String mit führenden Nullen aus.
    """
    try:
        counter_bytes = read_fram(0x01F0, 4)
        # Falls leer, initialisiere mit 0
        if not counter_bytes or not isinstance(counter_bytes, (bytes, bytearray)):
            counter_int = 0
        else:
            counter_int = int.from_bytes(counter_bytes, byteorder='big')
        counter_int += 1
        # Zurückschreiben als 4 Bytes
        write_fram(0x01F0, counter_int.to_bytes(4, byteorder='big'))
        # Ausgabe als vierstelliger String
        counter_str = f"{counter_int:04d}"
        print(f"Counter als String: {counter_str}")
        return counter_str
    except Exception as e:
        error_message(9, e)
        print(f"Power on counter konnte nicht erhöht werden: {e}")
        return None
def set_serial_number():
    """
    Funktion um die Seriennummer zu setzen
    """  
    try:
        SN = read_fram(0x0110, 8)
        write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "serielnumber", SN)
        print("Seriennummer in config geschrieben")
    except Exception as e:
        error_message(9,e)
        print("Seriennummer konnte nicht gesetzt werden")
        pass
    
def delete_error_code():
    """
    Funktion um den Error Code zu löschen
    """
    try:
        write_fram(0x1010,"0")  
        write_fram(0x1011,"0")    
        write_fram(0x1012,"0") 
        write_fram(0x1013,"0") 
        print("Fehlercode in FRAM auf 0 gesetzt")
    except Exception as e:
        error_message(9,e)
        print("Fehlercode in FRAM nicht gelöscht")
        
    try:
        write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "errorcode", "0")
        print("Fehlercode in config auf 0 gesetzt")
    except Exception as e:
        print("Fehlercode in config nicht gelöscht")
        pass
    
def store_times_power(power_on, power_off):
    """
    Funktion um die Zeiten für den Power on und Power off in den FRAM zu speichern
    """
    try:
        write_fram(0x0010, str(power_on))
        write_fram(0x0040, str(power_off))
        time.sleep(1)
        print("start time and stop time written to FRAM")
        log_schreiben("Start & Stop Zeiten im FRam aktualisiert")

    except Exception as e:
        error_message(9,"Fehler in der Kommunikation zwischen Raspberry Pi und Fram Modul. Zeiten für An und Ausschalten der Falle nicht aktualisiert.")
        time.sleep(5)
        
def check_version():
    """
    Funktion um die Version der Software zu überprüfen
    """
    Version_json = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "version")
    date_json = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "date")
    print(f"Software- Version: {Version_json} vom {date_json}")
    
    Version_fram = read_fram(0x0130, 8)
    date_fram = read_fram(0x0140, 8)
    if Version_fram != Version_json:
        write_fram(0x0130, Version_json)
        print("Version in FRAM aktualisiert")
    if date_fram != date_json:
        write_fram(0x0140, date_json)
        print("Datum in FRAM aktualisiert")