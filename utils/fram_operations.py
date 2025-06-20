from utils.json_read_write import *
from utils.log import log_schreiben
from utils.json_read_write import get_value_from_section, write_value_to_section
try:
    from utils.fram_direct import *
except Exception as e:
     print(f"Fehler beim Importieren von fram_direct: {e}")  
     
     
def ram_counter(ramadresse):
    """
    Liest eine 4-Byte-Zahl aus dem FRAM an der angegebenen Adresse, erhöht sie um 1 und schreibt sie zurück.
    Gibt den Wert als vierstelligen String mit führenden Nullen aus.
    """
    try:
        counter_bytes = read_fram_bytes(ramadresse, 4)
        # Falls leer, initialisiere mit 0
        if not counter_bytes or not isinstance(counter_bytes, (bytes, bytearray)):
            counter_int = 0
        else:
            counter_int = int.from_bytes(counter_bytes, byteorder='big')
        counter_int += 1
        # Zurückschreiben als 4 Bytes (jetzt korrekt als Bytes!)
        write_fram_bytes(ramadresse, counter_int.to_bytes(4, byteorder='big'))
        # Ausgabe als vierstelliger String
        counter_str = f"{counter_int:04d}"
        print(f"Counter an Adresse {hex(ramadresse)} als String: {counter_str}")
        return counter_str
    except Exception as e:
        print(f"Counter an Adresse {hex(ramadresse)} konnte nicht erhöht werden: {e}")
        return None
    
    
def set_serial_number():
    """
    Funktion um die Seriennummer zu setzen
    """  
    try:
        SN = read_fram(0x0110, 8)
        write_value_to_section(get_config_path("Lepmon_config.json"), "general", "serielnumber", SN)
        print("Seriennummer in config geschrieben")
    except Exception as e:
        try:
            SN = get_value_from_section(get_config_path("LepmonOS_serial_number.json"), "general", "serielnumber")
            print("Seriennummer aus JSON gelesen")
        except Exception as e:
            print("Seriennummer konnte nicht gesetzt werden")
            pass
    
def delete_error_code():
    """
    Funktion um den Error Code zu löschen
    """
    try:
        write_fram_bytes(0x1010, (0).to_bytes(4, byteorder='big'))
        print("Fehlercode in FRAM auf 0 gesetzt")
    except Exception as e:
        print("Fehlercode in FRAM nicht gelöscht")
        
    try:
        write_value_to_section(get_config_path("Lepmon_config.json"), "general", "errorcode", "0")
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
        time.sleep(5)
        
def check_version():
    """
    Funktion um die Version der Software zu überprüfen
    """
    Version_json = get_value_from_section(get_config_path("Lepmon_config.json"), "software", "version")
    date_json = get_value_from_section(get_config_path("Lepmon_config.json"), "software", "date")
    print(f"Software- Version: {Version_json} vom {date_json}")
    try:
        Version_fram = read_fram(0x0130, 8)
        date_fram = read_fram(0x0140, 8)
    except Exception as e:
        print(f"Fehler beim Lesen der Version/Daten aus dem FRAM: {e}")
        Version_fram = None
        date_fram = None
        return

    if Version_fram is not None and Version_json != Version_fram:
        write_fram(0x0130, Version_json)
        print("Version in FRAM aktualisiert")
    if Version_fram is not None and date_fram != date_json:
        write_fram(0x0140, date_json)
        print("Datum in FRAM aktualisiert")
        
        
if __name__ == "__main__":
    ram_counter(0x01F0)