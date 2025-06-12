from .OLED_panel import display_text
import time
from datetime import datetime
from .times import *
from .log import log_schreiben


def wait():
    
    experiment_start_time, experiment_end_time, LepiLed_end_time,time_buffer, lepi_led_buffer = get_experiment_times()
    _, lokale_Zeit = Zeit_aktualisieren()
    experiment_start_time = datetime.strptime(experiment_start_time, "%H:%M:%S")
    experiment_end_time = datetime.strptime(experiment_end_time, "%H:%M:%S")
    lokale_Zeit = datetime.strptime(lokale_Zeit, "%H:%M:%S")
    
    print(f"time buffer before dusk and after dawn: {time_buffer}")
    print(f"LepiLed_buffer: {lepi_led_buffer}")

    log_schreiben(f"Zeitpuffer vor Sonnenuntergang und Nach Sonnenaufgang: {time_buffer}")    
    log_schreiben(f"LepiLED wird {lepi_led_buffer} vor Sonnenaufgang ({experiment_end_time.strftime('%H:%M:%S')}) ausgeschaltet: {LepiLed_end_time}") 
    
    
    if not (experiment_end_time > lokale_Zeit >= experiment_start_time):
        print("Aktuelle Zeit liegt nach geplantem Nachtbeginn. Warte nicht sondern fahre fort")
        log_schreiben("Aktuelle Zeit liegt nach geplantem Nachtbeginn. Starte Schleife")
        pass

    elif (experiment_start_time - lokale_Zeit).total_seconds() >= 120 and (experiment_end_time > lokale_Zeit >= experiment_start_time):
        countdown = (experiment_start_time - lokale_Zeit).total_seconds()
        countdown_time = experiment_start_time - lokale_Zeit
        countdown = (experiment_start_time - lokale_Zeit).total_seconds()
        log_schreiben(f"warte bis Nachtbeginn: {countdown_time}")

        for _ in range(120):
            hours, remainder = divmod(int(countdown), 3600)  # Stunden berechnen
            minutes, seconds = divmod(remainder, 60)  # Minuten und Sekunden berechnen
            display_text("Beginne in", f"{hours:02d}:{minutes:02d}:{seconds:02d}", "")
            countdown -= 1  # Eine Sekunde abziehen
            time.sleep(1)
        _, lokale_Zeit = Zeit_aktualisieren() 
        difference = (experiment_start_time - lokale_Zeit).total_seconds()
        print(f"warten bis zum Experimentbeginn: {difference}")
        time.sleep(difference)



    elif 0< (experiment_start_time - lokale_Zeit).total_seconds() < 120 and (experiment_end_time > lokale_Zeit >= experiment_start_time):
        countdown = (experiment_start_time - lokale_Zeit).total_seconds()
        countdown_time = experiment_start_time - lokale_Zeit
        log_schreiben(f"warte bis Nachtbeginn: {countdown_time}")

        for _ in range(countdown):
            hours, remainder = divmod(int(countdown), 3600)  # Stunden berechnen
            minutes, seconds = divmod(remainder, 60)  # Minuten und Sekunden berechnen
            display_text("Beginne in", f"{hours:02d}:{minutes:02d}:{seconds:02d}", "")
            countdown -= 1  # Eine Sekunde abziehen
            time.sleep(1)        
