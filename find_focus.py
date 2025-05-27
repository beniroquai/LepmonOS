from OLED_panel import display_text
from Camera import get_frame
from GPIO_Setup import button_pressed
import time
import cv2
from error_handling import error_message
import sys
from Lights import *
from end import trap_shutdown
from GPIO_Setup import turn_on_led, turn_off_led


def set_exposure(Belichtungszeit):
    turn_on_led("blau")
    for _ in range(25):
        if button_pressed("oben"):
            if Belichtungszeit >20:
                Belichtungszeit += 10
            if Belichtungszeit <= 20:
                Belichtungszeit +=1

        if button_pressed("unten"):
            if Belichtungszeit >20:
                Belichtungszeit -= 10
            if Belichtungszeit <= 20:
                Belichtungszeit -=1
        if Belichtungszeit < 1:
                Belichtungszeit = 1        
        display_text("Belichtungszeit:",f"{Belichtungszeit} ms","jetzt fokusieren")         
        time.sleep(.1)   
    turn_off_led("blau")

    return Belichtungszeit

def focus():
    Belichtung_max = 20
    Belichtungszeit = 20
    sharpness = 0
    maximum = 0
    print("Fokusieren:\n"
          "Falle berechnet den schärsten Fokus, bassierend auf der 'Variance of Laplacian'\n" 
          "siehe https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/\n"
          "Fokusring drehen, bis der Schärfewert im Display sein Maximum erreicht hat")
    display_text("fokussieren","bis Anzeigewert","Maximum erreicht")
    time.sleep(5)
    FokusFehler = 0
    maximum = 0
    turn_on_led("gelb")
    while not button_pressed("enter"):
        display_text(f"Schärfewert: {sharpness}",f"Exposure: {Belichtungszeit} ms",f"peak: {maximum} @ {Belichtung_max}")
        dim_up()
        frame = get_frame(Belichtungszeit)
        dim_down()
        if frame is not None:
            FokusFehler = 0
        elif frame is None:
            FokusFehler += 1
            print("Fokussier fehler")
            
        if FokusFehler == 4:
            error_message(2,"Kamera mehrfach beim Fokussieren nicht initialisiert. Falle startet neu")
            display_text("Kamera überlastet","fokusieren nicht","beendet")
            time.sleep(3)
            display_text("nach Neustart","mit Fokusieren","fortfahren")
            time.sleep(3)
            trap_shutdown(5)

        print("analyse")

        if FokusFehler == 0:
            if frame is not None:
                display_text(f"Schärfewert: {sharpness}",f"peak: {maximum} @ {Belichtung_max}",f"set exposure {Belichtungszeit}")
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
                sharpness = round(cv2.Laplacian(gray, cv2.CV_64F).var(),0)
                turn_off_led("gelb")
                Belichtungszeit = set_exposure(Belichtungszeit)
                turn_on_led("gelb")
                if sharpness > maximum:
                    maximum = sharpness
                    Belichtung_max = Belichtungszeit

        print(f"aktueller Schärfeewert: {sharpness}\n"
              f"Maximum: {maximum}")
        

if __name__ == "__main__":
    focus()