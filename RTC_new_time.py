import time
from datetime import datetime
from GPIO_Setup import turn_on_led, turn_off_led, button_pressed
from OLED_panel import *
import adafruit_ds3231
from log import log_schreiben
from error_handling import error_message
import subprocess
import board
from service import RPI_time

i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

def input_time():
    print("Bitte Uhrzeit der Hardware Uhr Stellen")

    try:
        t = rtc.datetime
        time_string = f"{t.tm_year:04d}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"
        print(f"Aktuelle Hardware Uhrzeit: {time_string}")
        date_time_list = [int(digit) for digit in time_string if digit.isdigit()]
        print("datetimelist")
        print(date_time_list)
    except Exception as e:
        error_message(8, e)
        time.sleep(5)
        # Fallback: Default-Werte
        date_time_list = [2,0,2,4,0,1,0,1,0,0,0,0,0,0]

    aktuelle_position = 0
    Wahlmodus = 1  
    first_run = True  

    while True:
        turn_on_led("blau")
        if Wahlmodus == 1:
            if aktuelle_position < 4:
                positionszeiger_time = "_" * aktuelle_position
            elif 4 <= aktuelle_position < 6:
                positionszeiger_time = "_"*4 + "-" +"_" * (aktuelle_position-4)
            elif aktuelle_position >= 6:
                positionszeiger_time = "_"*4 + "-" + "_" *2 + "-" + "_" * (aktuelle_position-6)
            positionszeiger_time += "x"
            display_text_with_arrows("Datum einstellen", 
                                    f"{date_time_list[0]}{date_time_list[1]}{date_time_list[2]}{date_time_list[3]}-{date_time_list[4]}{date_time_list[5]}-{date_time_list[6]}{date_time_list[7]}",
                                    positionszeiger_time)

        elif Wahlmodus == 2:
            if first_run:
                time.sleep(1)  # Kurze Pause für die Stabilität
                first_run = False
            
            if 8 <= aktuelle_position <10:
                positionszeiger = "_" * (aktuelle_position-8)
            elif 10 <= aktuelle_position < 12:
                positionszeiger = "__:" + "_" * (aktuelle_position-10)
            elif aktuelle_position >=12 :
                positionszeiger = "__:__" + ":" + "_" * (aktuelle_position-12)
            positionszeiger += "x"
            display_text_with_arrows("Zeit einstellen",
                         f"{date_time_list[8]}{date_time_list[9]}:{date_time_list[10]}{date_time_list[11]}:{date_time_list[12]}{date_time_list[13]}",
                         positionszeiger)

        if button_pressed("oben"):
            # Begrenzung je nach Position
            if aktuelle_position == 4:  # Monat Zehnerstelle (max 1)
                date_time_list[4] = (date_time_list[4] + 1) % 2
                if date_time_list[4] == 1 and date_time_list[5] > 2:
                    date_time_list[5] = 2
            elif aktuelle_position == 5:  # Monat Einerstelle (max 9 oder 2)
                max_einer = 2 if date_time_list[4] == 1 else 9
                date_time_list[5] = (date_time_list[5] + 1) % (max_einer + 1)
            elif aktuelle_position == 6:  # Tag Zehnerstelle (max 3)
                date_time_list[6] = (date_time_list[6] + 1) % 4
                if date_time_list[6] == 3 and date_time_list[7] > 1:
                    date_time_list[7] = 1
            elif aktuelle_position == 7:  # Tag Einerstelle (max 9 oder 1)
                max_einer = 1 if date_time_list[6] == 3 else 9
                date_time_list[7] = (date_time_list[7] + 1) % (max_einer + 1)
            elif aktuelle_position == 8:  # Stunde Zehnerstelle (max 2)
                date_time_list[8] = (date_time_list[8] + 1) % 3
                if date_time_list[8] == 2 and date_time_list[9] > 3:
                    date_time_list[9] = 3
            elif aktuelle_position == 9:  # Stunde Einerstelle (max 9 oder 3)
                max_einer = 3 if date_time_list[8] == 2 else 9
                date_time_list[9] = (date_time_list[9] + 1) % (max_einer + 1)
            elif aktuelle_position == 10:  # Minute Zehnerstelle (max 5)
                date_time_list[10] = (date_time_list[10] + 1) % 6
            elif aktuelle_position == 11:  # Minute Einerstelle (max 9)
                date_time_list[11] = (date_time_list[11] + 1) % 10
            elif aktuelle_position == 12:  # Sekunde Zehnerstelle (max 5)
                date_time_list[12] = (date_time_list[12] + 1) % 6
            elif aktuelle_position == 13:  # Sekunde Einerstelle (max 9)
                date_time_list[13] = (date_time_list[13] + 1) % 10
            else:
                date_time_list[aktuelle_position] = (date_time_list[aktuelle_position] + 1) % 10

        elif button_pressed("unten"):
            # Begrenzung je nach Position
            if aktuelle_position == 4:  # Monat Zehnerstelle (max 1)
                date_time_list[4] = (date_time_list[4] - 1) % 2
                if date_time_list[4] == 1 and date_time_list[5] > 2:
                    date_time_list[5] = 2
            elif aktuelle_position == 5:  # Monat Einerstelle (max 9 oder 2)
                max_einer = 2 if date_time_list[4] == 1 else 9
                date_time_list[5] = (date_time_list[5] - 1) % (max_einer + 1)
            elif aktuelle_position == 6:  # Tag Zehnerstelle (max 3)
                date_time_list[6] = (date_time_list[6] - 1) % 4
                if date_time_list[6] == 3 and date_time_list[7] > 1:
                    date_time_list[7] = 1
            elif aktuelle_position == 7:  # Tag Einerstelle (max 9 oder 1)
                max_einer = 1 if date_time_list[6] == 3 else 9
                date_time_list[7] = (date_time_list[7] - 1) % (max_einer + 1)
            elif aktuelle_position == 8:  # Stunde Zehnerstelle (max 2)
                date_time_list[8] = (date_time_list[8] - 1) % 3
                if date_time_list[8] == 2 and date_time_list[9] > 3:
                    date_time_list[9] = 3
            elif aktuelle_position == 9:  # Stunde Einerstelle (max 9 oder 3)
                max_einer = 3 if date_time_list[8] == 2 else 9
                date_time_list[9] = (date_time_list[9] - 1) % (max_einer + 1)
            elif aktuelle_position == 10:  # Minute Zehnerstelle (max 5)
                date_time_list[10] = (date_time_list[10] - 1) % 6
            elif aktuelle_position == 11:  # Minute Einerstelle (max 9)
                date_time_list[11] = (date_time_list[11] - 1) % 10
            elif aktuelle_position == 12:  # Sekunde Zehnerstelle (max 5)
                date_time_list[12] = (date_time_list[12] - 1) % 6
            elif aktuelle_position == 13:  # Sekunde Einerstelle (max 9)
                date_time_list[13] = (date_time_list[13] - 1) % 10
            else:
                date_time_list[aktuelle_position] = (date_time_list[aktuelle_position] - 1) % 10

        elif button_pressed("rechts"):
            if Wahlmodus == 1:
                aktuelle_position = (aktuelle_position + 1) % 8
            elif Wahlmodus == 2:
                if aktuelle_position != 13:
                    aktuelle_position = (aktuelle_position + 1) % 14
                else:
                    aktuelle_position = 8

        elif button_pressed("enter"):
            Wahlmodus += 1
            aktuelle_position = 8
            display_text("","","")

        elif Wahlmodus >= 3:
            turn_off_led("blau")
            print("zeitbefehl erstellt")
            break

        time.sleep(0.05)  # Kurze Pause für die Stabilität
    turn_off_led("blau")    

    # Construct the command for setting system time
    system_time_str = f"{date_time_list[0]}{date_time_list[1]}{date_time_list[2]}{date_time_list[3]}-{date_time_list[4]}{date_time_list[5]}-{date_time_list[6]}{date_time_list[7]} {date_time_list[8]}{date_time_list[9]}:{date_time_list[10]}{date_time_list[11]}:{date_time_list[12]}{date_time_list[13]}"
    print("Eingegebener Zeitsring:", system_time_str)
    
    # Validierung der Eingabewerte
    jahr = int(f"{date_time_list[0]}{date_time_list[1]}{date_time_list[2]}{date_time_list[3]}")
    monat = int(f"{date_time_list[4]}{date_time_list[5]}")
    tag = int(f"{date_time_list[6]}{date_time_list[7]}")
    stunde = int(f"{date_time_list[8]}{date_time_list[9]}")
    minute = int(f"{date_time_list[10]}{date_time_list[11]}")
    sekunde = int(f"{date_time_list[12]}{date_time_list[13]}")
    return jahr, monat, tag, stunde, minute, sekunde, date_time_list

def check_date_time():
    jahr, monat, tag, stunde, minute, sekunde, _ = input_time()
    try:
        # Jahr prüfen
        if not (2025 <= jahr <= 2035):
            display_text("ungültiges Jahr, bitte neu eingeben","",3)       
            return False
        # Monat prüfen
        if not (1 <= monat <= 12):
            display_text("ungültiger Monat, bitte neu eingeben","",3)
            return False
        # Tag prüfen (einfach, ohne Monatslänge/Schaltjahr)
        if not (1 <= tag <= 31):
            display_text("ungültiger Tag, bitte neu eingeben","",3)
            return False
        # Stunde prüfen
        if not (0 <= stunde <= 23):
            display_text("ungültige Stunde, bitte neu eingeben","",3)
            return False
        # Minute prüfen
        if not (0 <= minute <= 59):
            display_text("ungültige Minute, bitte neu eingeben","",3)
            return False
        # Sekunde prüfen
        if not (0 <= sekunde <= 59):
            display_text("ungültige Sekunde, bitte neu eingeben","",3)
            return False
        # Optional: exakte Prüfung mit datetime (inkl. Monatslänge/Schaltjahr)
        datetime(jahr, monat, tag, stunde, minute, sekunde)
        return True
    except Exception:
        return False    
    
def set_hwc():
    _, _, _, _, _, _, date_time_list = input_time()
    while True:
        # Werte extrahieren
        jahr = int(f"{date_time_list[0]}{date_time_list[1]}{date_time_list[2]}{date_time_list[3]}")
        monat = int(f"{date_time_list[4]}{date_time_list[5]}")
        tag = int(f"{date_time_list[6]}{date_time_list[7]}")
        stunde = int(f"{date_time_list[8]}{date_time_list[9]}")
        minute = int(f"{date_time_list[10]}{date_time_list[11]}")
        sekunde = int(f"{date_time_list[12]}{date_time_list[13]}")
        # Prüfe Werte vor dem Setzen!
        if not (2000 <= jahr <= 2099 and 1 <= monat <= 12 and 1 <= tag <= 31 and 0 <= stunde <= 23 and 0 <= minute <= 59 and 0 <= sekunde <= 59):
            display_text("Ungültige Eingabe!", "Bitte erneut", "versuchen.",3)
            print("Ungültige Eingabe, bitte erneut versuchen.")
            _, _, _, _, _, _, date_time_list = input_time()
            continue
        try:
            rtc_time = time.struct_time((
                jahr, monat, tag, stunde, minute, sekunde,
                0,  # weekday (ignored by DS3231)
                -1, -1  # yearday, isdst (ignored)
            ))
            print("RTC wird gesetzt auf Systemzeit:", rtc_time)
            rtc.datetime = rtc_time
            RPI_time()
            log_schreiben(f"Hardware Uhrzeit gesetzt auf: {rtc_time.tm_year}-{rtc_time.tm_mon:02d}-{rtc_time.tm_mday:02d} {rtc_time.tm_hour:02d}:{rtc_time.tm_min:02d}:{rtc_time.tm_sec:02d}")
            break
        except Exception as e:
            error_message(8, e)
            display_text("Fehler beim Setzen", "der Uhrzeit!", "",3)
            _, _, _, _, _, _, date_time_list = input_time()
    time.sleep(0.5)

if __name__ == "__main__":
    set_hwc()