from datetime import datetime
from utils.json_read_write import get_value_from_section, get_config_path
from utils.lora import send_lora


def log_schreiben(text, mPath=None):
    """Schreibt den übergebenen Text in das Logfile."""
    lokale_Zeit = datetime.now()
    if mPath is None:
        mPath = get_config_path("Lepmon_config.json")
    try:
        log_dateipfad = get_value_from_section(mPath,"general","current_log")
    except Exception as e:
        send_lora(f"Fehler 11: Konfigurationsdatei 'Lepmon_config.json' nicht gefunden oder Wert fehlerhaft:{e}")
        return 
    
    try:
        with open(log_dateipfad, 'a') as f:
            f.write(f"{lokale_Zeit}; {text}" + '\n')
    except Exception as e:
        send_lora(f"Fehler 10: Logging File nicht gefunden und Eintrag nicht erstellt. Prüfe USB Stick:{e}")
