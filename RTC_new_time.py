import time
from datetime import datetime
from GPIO_Setup import turn_on_led, turn_off_led, button_pressed
from OLED_panel import display_text
import adafruit_ds3231
from log import log_schreiben
from error_handling import error_message
import subprocess
import board
from service import RPI_time
from end import trap_shutdown

i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)

def set_hwc():
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

    aktuelle_position = 0
    Wahlmodus = 1    

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
              
                display_text("Datum einstellen",
                             f"{date_time_list[0]}{date_time_list[1]}{date_time_list[2]}{date_time_list[3]}-{date_time_list[4]}{date_time_list[5]}-{date_time_list[6]}{date_time_list[7]}", 
                             positionszeiger_time)


            elif Wahlmodus == 2:
                if 8 <= aktuelle_position <10:
                   positionszeiger = "_" * (aktuelle_position-8)
                elif 10 <= aktuelle_position < 12:
                   positionszeiger = "__:" + "_" * (aktuelle_position-10)
                elif aktuelle_position >=12 :
                   positionszeiger = "__:__" + ":" + "_" * (aktuelle_position-12)
                positionszeiger += "x"

                display_text("Zeit einstellen",
                             f"{date_time_list[8]}{date_time_list[9]}:{date_time_list[10]}{date_time_list[11]}:{date_time_list[12]}{date_time_list[13]}",
                             positionszeiger)

        
            if button_pressed("oben"):
                date_time_list[aktuelle_position] = (date_time_list[aktuelle_position] + 1) % 10
            
            elif button_pressed("unten"):
                date_time_list[aktuelle_position] = (date_time_list[aktuelle_position] - 1) % 10
            
            elif button_pressed("rechts"):
                if Wahlmodus == 1:
                    aktuelle_position = (aktuelle_position + 1) % 8
                    aktuelle_position = aktuelle_position
                elif Wahlmodus == 2:
                    if aktuelle_position != 13:  # Anstatt 14, da die Positionen 8 bis 13 die Zeit HH:MM:SS repräsentieren
                        aktuelle_position = (aktuelle_position + 1) % 14
                        aktuelle_position = aktuelle_position
                    else:
                        aktuelle_position = 8  # Zurück zur Position 8 für Stunden (HH) wenn Sekunden (SS) bearbeitet wurden
                        aktuelle_position = aktuelle_position
        
            elif button_pressed("enter"):
                Wahlmodus += 1
                aktuelle_position = 8
                display_text("","","")
        
            elif Wahlmodus >= 3:
                turn_off_led("blau")
                print("zeitbefehl erstellt")
                break
                

            time.sleep(0.05)  # Kurze Pause für die Stabilität

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

    # Grenzen prüfen
    if not (2000 <= jahr <= 2099):
            msg = f"ungüliges Jahr {jahr}"
            error_message(8, f"{msg} --  Neustart erwartet")
            display_text(msg,"bitte neustarten","")   
            time.sleep(3)         
            trap_shutdown(5)
            raise ValueError(f"Jahr {jahr} außerhalb des gültigen Bereichs (2000–2099)")
            return        
    if not (1 <= monat <= 12):
            msg = f"ungüliger Monat {monat}"
            error_message(8, f"{msg} --  Neustart erwartet")
            display_text(msg,"bitte neustarten","")
            time.sleep(3)    
            trap_shutdown(5)
            raise ValueError(f"Monat {monat} ist ungültig")
            return
    if not (1 <= tag <= 31):  # Optional: Du kannst hier mit Kalenderlogik genauer sein
            msg = f"ungüliger Tag {tag}"
            error_message(8, f"{msg} --  Neustart erwartet")
            display_text(msg,"bitte neustarten","")
            time.sleep(3)    
            trap_shutdown(5)
            raise ValueError(f"Tag {tag} ist ungültig")
            return
    if not (0 <= stunde <= 23):
            msg = f"ungülige Stunde {stunde}"
            error_message(8, f"{msg} --  Neustart erwartet")
            display_text(msg,"bitte neustarten","")
            time.sleep(3)   
            trap_shutdown(5) 
            raise ValueError(f"Stunde {stunde} ist ungültig")
            return    
    if not (0 <= minute <= 59):
            msg = f"ungülige Minute {minute}"
            error_message(8, f"{msg} --  Neustart erwartet")
            display_text(msg,"bitte neustarten","")
            time.sleep(3)    
            trap_shutdown(5)
            raise ValueError(f"Minute {minute} ist ungültig")
            return            
    if not (0 <= sekunde <= 59):
            msg = f"ungültige Sekunde {sekunde}"
            error_message(8, f"{msg} --  Neustart erwartet")
            display_text(msg,"bitte neustarten","")
            time.sleep(3)    
            trap_shutdown(5)
            raise ValueError(f"Sekunde {sekunde} ist ungültig")
            return


    try:

        rtc_time = time.struct_time((
        int(f"{date_time_list[0]}{date_time_list[1]}{date_time_list[2]}{date_time_list[3]}"),  # year
        int(f"{date_time_list[4]}{date_time_list[5]}"),  # month
        int(f"{date_time_list[6]}{date_time_list[7]}"),  # day
        int(f"{date_time_list[8]}{date_time_list[9]}"),  # hour
        int(f"{date_time_list[10]}{date_time_list[11]}"),  # minute
        int(f"{date_time_list[12]}{date_time_list[13]}"),  # second
        0,  # weekday (ignored by DS3231)
        -1, -1  # yearday, isdst (ignored)
        ))

        print("RTC wird gesetzt auf Systemzeit:", rtc_time)
        rtc.datetime = rtc_time
        RPI_time()
        log_schreiben(f"Hardware Uhrzeit gesetzt auf: {rtc_time.tm_year}-{rtc_time.tm_mon:02d}-{rtc_time.tm_mday:02d} {rtc_time.tm_hour:02d}:{rtc_time.tm_min:02d}:{rtc_time.tm_sec:02d}")

    except Exception as e:
        error_message(8, e)
       

if __name__ == "__main__":
    set_hwc()