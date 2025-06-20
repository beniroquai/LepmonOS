# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from datetime import datetime, timedelta
import board
import adafruit_ds3231
from .error_handling import error_message
from .times import *

i2c = board.I2C()
rtc = adafruit_ds3231.DS3231(i2c)


def set_alarm(power_on, power_off):
    """
    Setzt den Alarm auf die RTC
    :param alaram: 1 oder 2
    :param timestring: String im Format "YYYY-MM-DD HH:MM:SS"
    """
    try:
        alarm1_time = time.strptime(power_on, "%Y-%m-%d %H:%M:%S")
        rtc.alarm1 = (alarm1_time, "daily")
        rtc.alarm1_status = False
        rtc.alarm1_interrupt = True
        print("Alarm 1 gesetzt auf:", time.strftime("%Y-%m-%d %H:%M:%S", alarm1_time))

        alarm2_time = time.strptime(power_off, "%Y-%m-%d %H:%M:%S")
        rtc.alarm2 = (alarm2_time, "daily")
        rtc.alarm2_interrupt = True
        print("Alarm 2 gesetzt auf:", time.strftime("%Y-%m-%d %H:%M:%S", alarm2_time))
    
    except Exception as e:
        error_message(8, e)


if __name__ == "__main__":
    now_str, _ = Zeit_aktualisieren()  # Angenommen, Zeit_aktualisieren gibt einen String zurück
    now = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")  # Konvertiere den String in ein datetime-Objekt

    now_plus_one_minute = (now + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
    now_plus_one_day = (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    set_alarm(now_plus_one_minute, now_plus_one_day)
    
    i = 1
    while True:
        print(i)
        i += 1
        time.sleep(1)
        
        if rtc.alarm1_status:
            print("Alarm 1 ausgelöst!")
            rtc.alarm1_status = False
            print("Ende des Alarm Tests")
            break