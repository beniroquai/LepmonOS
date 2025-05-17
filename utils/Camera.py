from vimba import *
from Lights import dim_up, dim_down
from json_read_write import get_value_from_section
import time
from datetime import datetime
import os
import cv2
from OLED_panel import display_text
from log import log_schreiben
from GPIO_Setup import button_pressed
from sensor_data import read_sensor_data
from error_handling import error_message
IS_IMSWITCH = True
try:
    project_name = get_value_from_section("./config/Lepmon_config.json","general","project_name")
    sensor_id = get_value_from_section("./config/Lepmon_config.json","general","serielnumber")
    province = get_value_from_section("./config/Lepmon_config.json","locality","province")
    city_code = get_value_from_section("./config/Lepmon_config.json","locality","city")
except Exception as e:
    error_message(11,e)

         

def get_frame_vimba(Exposure):
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()

        try:
            with cams[0] as cam:
                formats = cam.get_pixel_formats()
                #print("Unterstützte Pixelformate:", formats)

                cam.set_pixel_format(PixelFormat.Bgr8)

                settings_file = '/home/pi/LepmonOS/Kamera_Einstellungen.xml'.format(cam.get_id())
                cam.load_settings(settings_file, PersistType.All)

                
                exposure_time = cam.ExposureTime
                exposure_time.set(Exposure*1000)
                print(f"Exposure geändert:{(exposure_time.get()/1000):.0f}")
                
                frame = cam.get_frame_vimba(timeout_ms=5000).as_opencv_image()
                
        except Exception as e:
                    error_message(1,e)
                    time.sleep(3)
                    print(f"Fehler beim Abrufen des Frames: {e}")
                    frame = None
                    print(f"'Frame: {frame}'")
            
        return frame
        
#####################




def snap_image(file_extension,mode,Kamera_Fehlerserie,Exposure):
    """
    nimmt ein Bild auf

    :param file_extension: Dateierweiterung
    :param mode: "display" für lokale ausgabe oder "log" für speichern in der schleife
    """
    ordnerpfad = get_value_from_section("./config/Lepmon_config.json","general","current_folder")
    now = datetime.now()
    code = f"{project_name}{sensor_id}_{province}_{city_code}_{now.strftime('%Y')}-{now.strftime('%m')}-{now.strftime('%d')}_T_{now.strftime('%H%M')}"
    image_file = f"{code}.{file_extension}"
    dateipfad = os.path.join(ordnerpfad, image_file)

    dim_up()

    print("dimme LED hoch")
    if mode == "display":
        display_text("Dimme LED","hoch","")
        ordnerpfad = "/home/pi/LepmonOS/"
        power_on = 0

    if IS_IMSWITCH:
        import imswitchclient.ImSwitchClient as imc
        client = imc.ImSwitchClient(host="localhost", isHttps=True, port=8001)
        # client.recordingManager.setExposureTime(Exposure)
        # client.recordingManager.setGain(mGain)
        frame = client.recordingManager.snapNumpyToFastAPI()
    else:
        frame = get_frame_vimba(Exposure)

    if frame is not None:
        Kamera_Fehlerserie = 0

    if frame is None and mode == "display":
        #display_text("Kamera Fehler5","bitte USB","Kabel prüfen")
        error_message(1,e)

    if frame is None and mode == "log": 
        Status_Kamera = 0   
        Kamera_Fehlerserie += 1

    if mode == "log":
        power_on = read_sensor_data("LED-an","now")
        power_on = power_on["power"]
        
    dim_down()

    print("dimme LED runter")
    if mode == "display":
        display_text("Dimme LED","herunter","")

    try:
        cv2.imwrite(dateipfad, frame)
        print(f"Bild gespeichert: {dateipfad}")
        Status_Kamera = 1
        if mode == "display":
            display_text("Bild","gespeichert","")
            time.sleep(.5)
            os.remove(dateipfad)
            time.sleep(.1)
            print(f"Bild vom Speicher gelöscht: {dateipfad}")
            log_schreiben("Kamera Zugriff erfolgreich")
        if mode == "log": 
            log_schreiben(f"Bild gespeichert: {dateipfad}")             

    except Exception as e:
        error_message(1,e)
        Status_Kamera = 0   

    return code, dateipfad, Status_Kamera, power_on, Kamera_Fehlerserie   



if __name__ == "__main__":
    print("Starte Kamera...")
    snap_image("jpg","log",0)                