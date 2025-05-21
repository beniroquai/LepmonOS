from datetime import datetime
from json_read_write import get_value_from_section
from lora import send_lora


def log_schreiben(text):
    """Schreibt den übergebenen Text in das Logfile."""
    lokale_Zeit = datetime.now().strftime("%H:%M:%S")
    try:
        log_dateipfad = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json","general","current_log")
    except Exception as e:
        send_lora(f"Fehler 11: Konfigurationsdatei 'Lepmon_config.json' nicht gefunden oder Wert fehlerhaft:{e}")
        return 
    
    try:
        with open(log_dateipfad, 'a') as f:
            f.write(f"{lokale_Zeit}; {text}" + '\n')
    except Exception as e:
        send_lora(f"Fehler 10: Logging File nicht gefunden und Eintrag nicht erstellt. Prüfe USB Stick:{e}")


if __name__ == "__main__":
    print("Logfile wird geschrieben") 