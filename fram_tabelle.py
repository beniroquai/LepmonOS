from fram_direct import read_fram, read_fram_bytes
from tabulate import tabulate
import time
from datetime import datetime, timedelta

def decode_bytes(data):
    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        try:
            text = data.decode("utf-8").strip('\x00')
            if text and all(32 <= ord(c) < 127 for c in text):
                return text
        except Exception:
            pass
        if len(data) <= 4:
            try:
                return int.from_bytes(data, "big")
            except Exception:
                pass
        return " ".join(f"{b:02X}" for b in data)
    return str(data)

def format_runtime(secs):
    try:
        secs = int(secs)
        minutes, sec = divmod(secs, 60)
        hours, minute = divmod(minutes, 60)
        days, hour = divmod(hours, 24)
        years, day = divmod(days, 365)
        months, day = divmod(day, 30)
        return f"{years}y {months}m {day}d {hour}h {minute}min"
    except Exception:
        return str(secs)

def format_timestamp(ts):
    try:
        ts = int(ts)
        dt = datetime.fromtimestamp(ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)

def format_gb(val):
    try:
        gb = int(val) / 1024 / 1024 / 1024
        return f"{gb:.1f} GB"
    except Exception:
        return str(val)

if __name__ == "__main__":
    werte = []

    werte.append(("Power_ON", decode_bytes(read_fram_bytes(0x0010,16))))
    werte.append(("Power_OFF", decode_bytes(read_fram_bytes(0x0040,16))))
    werte.append(("Serialnumber", decode_bytes(read_fram(0x0110,8))))
    werte.append(("Fallen_Version", decode_bytes(read_fram(0x0130,9))))
    werte.append(("Backplane", decode_bytes(read_fram(0x0150,15))))
    werte.append(("Lieferdatum", decode_bytes(read_fram(0x0170,10))))
    werte.append(("Boot_counter", decode_bytes(read_fram_bytes(0x0310,4))))
    werte.append(("User_Interface_counter", decode_bytes(read_fram_bytes(0x0330,4))))

    # total_runtime
    total_runtime_raw = decode_bytes(read_fram_bytes(0x0350,4))
    werte.append(("total_runtime", format_runtime(total_runtime_raw)))

    # timestamp_last_start
    ts_last_start_raw = decode_bytes(read_fram_bytes(0x0370,4))
    werte.append(("timestamp_last_start", format_timestamp(ts_last_start_raw)))

    # Gigabytes_free_at_start
    gb_free_raw = decode_bytes(read_fram_bytes(0x0390,4))
    werte.append(("Gigabytes_free_at_start", format_gb(gb_free_raw)))

    werte.append(("Software_Date", decode_bytes(read_fram(0x0510,10))))
    werte.append(("Software_Version", decode_bytes(read_fram(0x0520,5))))
    werte.append(("aktueller_Fehler", decode_bytes(read_fram_bytes(0x0810,4))))

    # Fehler-Tabelle
    for i, addr in enumerate(range(0x0840, 0x09D0, 0x20), 1):
        werte.append((f"Fehler {i:02d}", decode_bytes(read_fram_bytes(addr, 4))))
        time.sleep(.1)

    print(tabulate(werte, headers=["Label", "Wert"], tablefmt="github"))