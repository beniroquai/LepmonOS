from OLED_panel import display_text
from log import log_schreiben
from lora import send_lora
from json_read_write import write_value_to_section
try:
    from fram_direct import *
except ImportError:
    print("FRAM module not found. Skipping FRAM related operations.")
    pass

Display_MESSAGES = {
    1: ("Kamera - Prüfe", "Kabelverbindung", "Fehler 1"),
    2: ("Kamera wiederholt", "nicht initialisiert", "Fehler 2"),
    3: ("USB Stick - Prüfe", "Anschluss", "Fehler 3"),
    4: ("Lichtsensor - Prüfe", "Sensorkabel", "Fehler 4"),
    5: ("Außensensor - Prüfe", "Sensorkabel", "Fehler 5"),
    6: ("Innensensor", "Platinenfehler", "Fehler 6"),
    7: ("Stromsensor", "Platinenfehler", "Fehler 7"),
    8: ("Hardware Uhr", "Prüfe Zeit", "Fehler 8"),
    9: ("FRam", "Platinenfehler", "Fehler 9"),
    10: ("Logging", "Prüfe USB", "Fehler 10"),
    11: ("Checksumme nicht", "ermittelt", "Fehler 11"),
    12: ("Beleuchtungs LED", "verdunkelt", "Fehler 12"),
    13: ("Metadaten Tabelle", "Software/ USB Fehler", "Fehler 13"),
}

Logging_MESSAGES = {
    1: ("Fehler beim Abrufen des Frames - Bild nicht gespeichert. Prüfe Kamera-USB Kabel:", "Fehler 1"),
    2: ("kamera wiederholt nicht initialisiert. Falle startet neu zur Fehlerbehandlung", "Fehler 2"),
    3: ("USB Stick nicht gefunden. Anschluss prüfen", "Fehler 3"),
    4: ("Fehler in der Verbindung zum Lichtsensor. Wert des Umgebungslichtes auf Schwellenwert gesetzt: 90", "Fehler 4"),
    5: ("Fehler in der Verbindung zum Umweltsensor", "Fehler 5"),
    6: ("Fehler in der Verbindung zum Innen-Temperatursensor:", "Fehler 6"),
    7: ("Fehler in der Verbindung zum Stromsensor. Kein Monitoring der LED möglich:", "Fehler 7"),
    8: ("Fehler in der Verbindung zur HardwareUhr. Prüfe Kabelverbindung, Batterie oder eingegebenen Zeitstring", "Fehler 8"),
    9: ("Fehler in der Kommunikation zwischen Raspberry Pi und Fram Modul", "Fehler 9"),
    10: ("Logging File nicht gefunden und Eintrag nicht erstellt", "Fehler 10"),
    11: ("Checksumme für Bild,logfile oder Metadatentabelle nicht ermittelt", "Fehler 11"),
    12: ("Beleuchtungs LED ist verdunkelt. Leistung LepiLED (in W):", "Fehler 12"),
    13: ("Aktuelle Daten konnten nicht in Metadaten Tabelle geschrieben werden", "Fehler 13"),
}

# Separate function for Display_MESSAGES
def get_display_message(error_number):
    return Display_MESSAGES.get(error_number, ("Unbekannter Fehler", "Keine Details verfügbar", f"Fehler {error_number}"))

# Separate function for Logging_MESSAGES
def get_log_message(error_number):
    return Logging_MESSAGES.get(error_number, ("Unbekannter Fehler", f"Fehler {error_number}"))

def error_message(error_number, error_details):
    """
    Zeigt die Fehlermeldung auf dem Display an, loggt sie und sendet sie per LoRa.
    :param error_number: Fehlernummer (int)
    """
    text1, text2, text3 = get_display_message(error_number)  # Get display message
    logging_text, _ = get_log_message(error_number)  # Get log message (only need the first element)
    try:
        display_text(text3, text1, text2)  # Zeige die Fehlermeldung auf dem Display an
    except Exception as e:
        pass
    try:
        log_schreiben(f"Fehler {error_number}: {logging_text}: {error_details}")  # Logge die Fehlermeldung
    except Exception as e:
        pass   
    try:
        send_lora(f"Fehler {error_number}: {logging_text} {error_details}")  # Sende die Fehlermeldung per LoRa
    except Exception as e:
        pass
    
    try:
        write_fram(0x1010, str(error_number))  # Schreibe die Fehlernummer in den FRAM
    except Exception as e:  
        print(f"Fehler beim Schreiben in den FRAM: {e}")
        pass
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "errorcode", error_number)
    
def show_errors():
    """
    Beispiel: Zeigt alle Fehler aus der Liste an.
    """
    for error_number in Display_MESSAGES.keys():
        error_message(error_number, "detail")

if __name__ == "__main__":
    show_errors()
