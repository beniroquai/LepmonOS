import json
import os 

def get_project_root():
    """
    Get the project root directory path.
    
    Returns:
        str: Absolute path to the project root directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up from utils to project root
    return current_dir.split("utils")[0]

def get_config_path(config_file):
    """
    Get the full path to a config file.
    
    Args:
        config_file (str): Name of the config file (e.g., "Lepmon_config.json")
        
    Returns:
        str: Full path to the config file
    """
    return os.path.join(get_project_root(), "config", config_file)

def read_json(file_path):
    """
    Reads and returns the entire JSON content from a file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Parsed JSON data or None if error occurs
    """
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
        return None
    except json.JSONDecodeError as e:
        print(f"Fehler beim Parsen der JSON-Datei: {e}")
        return None
    except Exception as e:
        print(f"Fehler beim Lesen der JSON-Datei: {e}")
        return None


def write_json(file_path, data):
    """
    Writes data to a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        data (dict): Data to write to the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        return True
    except Exception as e:
        print(f"Fehler beim Schreiben der JSON-Datei: {e}")
        return False


def get_value_from_section(file_path, section_name, key_name):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # JSON-Datei öffnen und laden
        with open(os.path.join(current_dir.split("utils")[0], file_path), "r") as json_file:
            data = json.load(json_file)
        
        # Prüfen, ob die Sektion existiert
        if section_name in data:
            section = data[section_name]
            # Prüfen, ob der Schlüssel in der Sektion existiert
            if key_name in section:
                return section[key_name]  # Wert des Schlüssels zurückgeben
            else:
                return f"Der Schlüssel '{key_name}' existiert nicht in der Sektion '{section_name}'."
        else:
            return f"Die Sektion '{section_name}' existiert nicht in der Datei."
    except FileNotFoundError:
        return f"Die Datei {file_path} wurde nicht gefunden."
    except json.JSONDecodeError as e:
        return f"Fehler beim Parsen der JSON-Datei: {e}"
    except Exception as e:
        return f"Fehler: {e}"

def get_coordinates():
    latitude = get_value_from_section(get_config_path("Lepmon_config.json"), "GPS", "latitude")
    longitude = get_value_from_section(get_config_path("Lepmon_config.json"), "GPS", "longitude")
    Pol = get_value_from_section(get_config_path("Lepmon_config.json"), "GPS", "Pol")
    Block = get_value_from_section(get_config_path("Lepmon_config.json"), "GPS", "Block")

    if Pol == "N":
        Pol = ""
    elif Pol == "S":
        Pol = "-"

    if Block == "E":
        Block = ""
    elif Block == "W":  
        Block = "-"

    latitude = float(Pol + str(latitude))    
    longitude = float(Block + str(longitude))   

    return latitude, longitude, Pol, Block


def write_value_to_section(file_path, section_name, key_name, value):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        # JSON-Datei laden oder erstellen, falls sie nicht existiert
        try:
            with open(os.path.join(current_dir.split("utils")[0],file_path), "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}  # Leeres Dictionary, falls die Datei nicht existiert

        # Sicherstellen, dass die Sektion existiert
        if section_name not in data:
            data[section_name] = {}

        # Wert in der Sektion setzen
        data[section_name][key_name] = value

        # JSON-Datei speichern
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        return f"Wert '{value}' erfolgreich in Sektion '{section_name}' unter Schlüssel '{key_name}' geschrieben."
    except json.JSONDecodeError as e:
        return f"Fehler beim Parsen der JSON-Datei: {e}"
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}"


if __name__ == "__main__":
    get_coordinates()
    print("Koordinaten abgefragt")