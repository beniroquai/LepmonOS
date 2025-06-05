import shutil
import os
from service import get_usb_path
from times import Zeit_aktualisieren
import subprocess
from fram_direct import *
from OLED_panel import display_text
import time
from json_read_write import get_value_from_section
from log import log_schreiben
from end import trap_shutdown

def update_LepmonOS():
    usb_mount = get_usb_path()
    Version = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "version")
    timestamp,_ ,_ = Zeit_aktualisieren()
    update_folder = os.path.join(usb_mount, "LepmonOS_update")
    target_folder = "/home/Ento/LepmonOS"
    backup_folder = target_folder + f"_backup_{Version}__{timestamp}"

    if os.path.exists(update_folder):
        display_text("Update-Ordner", "gefunden","",2)
        print("Update-Ordner gefunden. Starte Update...")
        if os.path.exists(backup_folder):
            shutil.rmtree(backup_folder)
            
        print(f"Sichere aktuelles LepmonOS in {backup_folder}...") 
        shutil.copytree(target_folder, backup_folder)
        log_schreiben(f"altes Programm im Ordner {backup_folder} hinterlegt")         
        
        print("Lösche altes LepmonOS...")
        shutil.rmtree(target_folder)
        log_schreiben("alter Programmordner gelöscht")  
                
        print("Kopiere neues LepmonOS...")
        shutil.copytree(update_folder, target_folder)
        log_schreiben("neue LepmonOS Version geladen")          
        
        print("Update abgeschlossen")
    else:
        print("Kein Update-Ordner auf USB-Stick gefunden.")
        display_text("Update-Ordner", "nicht gefunden","",2)
        log_schreiben("kein Update gefunden")
        
           
def is_valid_update_stick():
    usb_mount = get_usb_path()
    marker_file = os.path.join(usb_mount, "LEPMON_UPDATE.KEY")
    if not os.path.exists(marker_file):
        print("LEPMON_UPDATE.KEY Datei nicht gefunden.")
        display_text("Schlüsseldatei", "nicht gefunden","",2)
        return False
    with open(marker_file, "r") as f:
        content = f.read()
        print(f"LEPMON_UPDATE.KEY Datei gefunden. Inhalt: {content} Fahre mit Update fort")
        display_text("Schlüsseldatei", "gefunden","",1)
    return "LEPMON-UPDATE-KEY-2025" in content

def get_new_version_from_stick():
    usb_mount = get_usb_path()
    version_file = os.path.join(usb_mount, "version.txt")
    if not os.path.exists(version_file):
        print("Keine version.txt auf dem Stick gefunden!")
        return None
    with open(version_file, "r") as f:
        return f.read().strip()
    
def get_current_version():
    # Lies die aktuelle Version aus dem FRAM (als String)
    try:
        current_version = read_fram(0x0520, 5)
    except Exception as e:
        current_version = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "version")
    if current_version:
        return current_version.strip()
    return None

def version_tuple(version_str):
    return tuple(map(int, version_str.strip().split(".")))

def is_update_allowed():
    new_version = get_new_version_from_stick()
    current_version = get_current_version()
    if not new_version or not current_version:
        print("Konnte Version nicht lesen.")
        display_text("neue Version", "nicht gefunden","")
        log_schreiben("neue Version nicht gefunden",2)
        return False
    if version_tuple(new_version) == version_tuple(current_version):
        print("Version ist gleich, Update nicht nötig.")
        display_text("Software Version", "bereits aktuell","",2)
        log_schreiben("Software Version bereits aktuell")
        return False
    elif version_tuple(new_version) < version_tuple(current_version):
        print("Downgrade nicht erlaubt!")
        display_text("Downgrade", "nicht erlaubt","",2)
        log_schreiben("Downgrade nicht erlaubt")
        return False
    else:
        print("Update erlaubt!")
        return True

def update():
    display_text("LepmonOS Update", "Starte Update...", "Bitte warten...")
    log_schreiben("Menü zum Updaten geöffnet")
    time.sleep(2)
    if is_valid_update_stick() and is_update_allowed():
        print("Update-Stick ist gültig und Update erlaubt.")
        log_schreiben("Update-Stick ist gültig und Update erlaubt.")
        try:
            print("Starte LepmonOS Update...")
            display_text("Update", "wird gestartet", "")
            update_LepmonOS()
            print("Update erfolgreich!")
            display_text("Update", "erfolgreich","",1)
            new_version = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "version")
            new_date = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "software", "date")
            print(f"Neue Version: {new_version} vom {new_date}")
            display_text("Neue Version:", new_version, new_date,3)
            log_schreiben(f"neue Softwareversion:{new_version}")
            write_fram(0x0520, new_version.ljust(7))  # Update die Version im FRAM
            write_fram(0x0510, new_date.ljust(10))  # Update das Datum im FRAM
            print("Version im FRAM aktualisiert.")
            log_schreiben("starte neu")
            display_text("Update installiert","Falle startet neu","",2)
            trap_shutdown(5)

        except Exception as e:
            print(f"Fehler beim Update: {e}")
            display_text("Kein Update", "durchgeführt", "fahre fort",3)
            log_schreiben(f"Fehler beim update:{e}")
            return
    else:
        print("Update nicht erlaubt oder kein gültiger Update-Stick gefunden.")
        log_schreiben("Update nicht erlaubt oder kein gültiger Update-Stick gefunden.")


if __name__ == "__main__":
    update()
                