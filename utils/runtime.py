import time
from utils.fram_operations import*



def get_unix_time():
    return int(time.time())

def write_runtime_start():
    # Schreibe aktuellen Unix-Zeitstempel ins FRAM (4 Byte)
    write_fram_bytes(0x0370, get_unix_time().to_bytes(4, 'big'))

def read_runtime_start():
    # Lese Unix-Zeitstempel aus dem FRAM
    return int.from_bytes(read_fram_bytes(0x0370, 4), 'big')

def write_total_runtime(total_seconds):
    write_fram_bytes(0x0350, int(total_seconds).to_bytes(4, 'big'))

def read_total_runtime():
    return int.from_bytes(read_fram_bytes(0x0350, 4), 'big')

def on_start():
    now = get_unix_time()
    try:
        last_start = read_runtime_start()
        total_runtime = read_total_runtime()
    except Exception as e:
        print("Fehler beim Lesen der Laufzeitdaten:", e)
        last_start = 0
        total_runtime = 0

    # Prüfe, ob ein alter Startwert existiert (Gerät wurde nicht sauber beendet)
    if last_start > 0 and last_start < now:
        # Zeit seit letztem Start addieren
        diff = now - last_start
        total_runtime += diff
        try:
            write_total_runtime(total_runtime)
            print(f"Unsauberer Shutdown erkannt, {diff} Sekunden nachgetragen.")
        except Exception as e:
            print("Fehler beim Schreiben der Laufzeit:", e)
            total_runtime = 0

    # Schreibe neuen Startzeitpunkt
    try:
        write_runtime_start()
        print(f"Startzeitpunkt {now} gespeichert.")
    except Exception as e:
        print("Fehler beim Schreiben des Startzeitpunkts:", e)


def on_shutdown():
    now = get_unix_time()
    try:
        last_start = read_runtime_start()
        total_runtime = read_total_runtime()
    except Exception as e:
        print("Fehler beim Lesen der Laufzeitdaten:", e)
        last_start = None
        total_runtime = None
    if last_start is not None and last_start > 0 and last_start < now:
        diff = now - last_start
        total_runtime += diff
        write_total_runtime(total_runtime)
        print(f"Laufzeit {diff} Sekunden hinzugefügt.")
