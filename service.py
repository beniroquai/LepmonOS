import os
from datetime import datetime
from json_read_write import *
from times import *
import hashlib
from error_handling import error_message
import time
from times import *
import subprocess

try:
    project_name = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json","general","project_name")
    sensor_id = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json","general","serielnumber")
    print(f"Sensor ID: {sensor_id}")
    province = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json","locality","province")
    city_code = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json","locality","city")
except Exception as e:
    error_message(11,e)
    


def get_usb_path():
    """Ermittelt den Pfad des USB-Sticks."""
    zielverzeichnis = ""
    username = os.getenv('USER')
    media_path = f"/media/{username}"
    if os.path.exists(media_path):
        for item in os.listdir(media_path):
            zielverzeichnis = os.path.join(media_path, item)
            if os.path.ismount(zielverzeichnis):
                USB_PATH = zielverzeichnis
                print(f"USB stick gefunden: {zielverzeichnis}")
                return zielverzeichnis
    return None          
            
def erstelle_ordner():
    zielverzeichnis = get_usb_path()
    jetzt_local, _, _ = Zeit_aktualisieren()
    jetzt_local = datetime.strptime(jetzt_local, "%Y-%m-%d %H:%M:%S")
    #jetzt_local = datetime.now()
    ordnername = f"{project_name}{sensor_id}_{province}_{city_code}_{jetzt_local.strftime('%Y')}-{jetzt_local.strftime('%m')}-{jetzt_local.strftime('%d')}_T_{jetzt_local.strftime('%H%M')}"
    aktueller_nachtordner = None
    try:
        if aktueller_nachtordner is None or not os.path.exists(aktueller_nachtordner):
            aktueller_nachtordner = os.path.join(zielverzeichnis, ordnername)
            os.makedirs(aktueller_nachtordner, exist_ok=True)
            print(f"Ordner erstellt: {aktueller_nachtordner}")
            write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_folder",aktueller_nachtordner)
            print("Pfad des Ausgabe Ordner in der Konfigurationsdatei gespeichert")
            return aktueller_nachtordner
    except Exception as e:
        error_message(3,e)
        return aktueller_nachtordner
        


def initialisiere_logfile():
  aktueller_nachtordner = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json","general","current_folder")
  #jetzt_local = datetime.now()
  #lokale_Zeit = jetzt_local.strftime("%H:%M:%S")
  jetzt_local, lokale_Zeit,_ = Zeit_aktualisieren()
  
  ordnername = os.path.basename(aktueller_nachtordner)
  log_dateiname = f"{ordnername}.log"
  log_dateipfad = os.path.join(aktueller_nachtordner, log_dateiname)
  
  try:
        # Initiales Erstellen des Logfiles
        if not os.path.exists(log_dateipfad):
            with open(log_dateipfad, 'w') as f:
                f.write(f"{lokale_Zeit}; Logfile erstellt: {log_dateipfad}\n")
                print(f"logdatei erstellt:{log_dateipfad}")
                write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "general", "current_log",log_dateipfad)
                print(f"Pfad der Logdatei in der Konfigurationsdatei gespeichert")
  except Exception as e:
        lokale_Zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{lokale_Zeit}; Fehler beim Erstellen des Logfiles: {e}")
        return None

def get_disk_space(): ####Speicher Abfrage####
    path = get_usb_path()
    try:
        stat = os.statvfs(path) # Erhalte Informationen über den Dateisystemstatus
        total_space = stat.f_frsize * stat.f_blocks # Gesamtgröße des Dateisystems in Bytes
        used_space = stat.f_frsize * (stat.f_blocks - stat.f_bfree) # Verwendeter Speicherplatz in Bytes
        free_space = stat.f_frsize * stat.f_bavail # Freier Speicherplatz in Bytes
        
        # Konvertiere Bytes in GB
        total_space_gb = round(total_space / (1024 ** 3), 2)
        used_space_gb = round(used_space / (1024 ** 3), 2)
        free_space_gb = round(free_space / (1024 ** 3), 2)
        
        used_percent = round((used_space / total_space) * 100, 2) # Berechne Prozentanteil des belegten und freien Speicherplatzes
        free_percent = round((free_space / total_space) * 100, 2)


        print(f"Speicher gesamt:{total_space_gb }")
        print(f"Speicher belegt:{used_space_gb}")
        print(f"Speicher frei:{free_space_gb}")
        print(f"Speicher belegt:{used_percent}")
        print(f"Speicher frei:{free_percent}")

        return total_space_gb, used_space_gb, free_space_gb, used_percent, free_percent
    except Exception as e:
        log_schreiben(f"Fehler beim Abrufen des Speicherplatzes: {e}")
        return None, None, None, None, None   


def checksum(dateipfad, algorithm="md5"):
  try:
    if not os.path.exists(dateipfad):  # Prüfe, ob die Datei existiert
      raise FileNotFoundError(f"Datei nicht gefunden: {dateipfad}")

    hash_func = hashlib.new(algorithm)  # Erstelle ein neues Hash-Objekt
    
    with open(dateipfad, "rb") as file: # Datei im Binärmodus lesen und Hash aktualisieren
      while chunk := file.read(8192):  # Datei in 8-KB-Blöcken lesen
        hash_func.update(chunk)
 
    checksum = hash_func.hexdigest() # Prüfsumme als Hex-String
  
    dir_name = os.path.dirname(dateipfad) # Erzeuge den Pfad für die Prüfsummen-Datei
    base_name = os.path.basename(dateipfad)
    checksum_file_name = f"{base_name}.{algorithm}"
    checksum_dateipfad = os.path.join(dir_name, checksum_file_name)
  
    with open(checksum_dateipfad, "w") as checksum_file:
      checksum_file.write(checksum) # Prüfsumme in der Datei speichern
  
  except Exception as e:
     error_message(11,e)


def RPI_time():
    """
    Funktion um die Zeit des Raspberry Pi zu setzen
    """
    jetzt_local,_ ,_= Zeit_aktualisieren()
    try:
        subprocess.run(['sudo', 'date', "-s", jetzt_local])
        print(f"Uhrzeit des Pi auf {jetzt_local} gestellt")
    except Exception as e:
        print(f"Fehler beim Stellen der RPi Uhr: {e}") 
        
        
if __name__ == "__main__":

    print("test")