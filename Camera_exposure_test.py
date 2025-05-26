from vimba import *
from Lights import dim_up, dim_down
from json_read_write import get_value_from_section
import time
import os
import cv2
from service import get_usb_path

def get_frame(Exposure):
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()

        try:
            with cams[0] as cam:
                formats = cam.get_pixel_formats()
                #print("Unterstützte Pixelformate:", formats)

                cam.set_pixel_format(PixelFormat.Bgr8)

                settings_file = '/home/Ento/LepmonOS/Kamera_Einstellungen.xml'.format(cam.get_id())
                cam.load_settings(settings_file, PersistType.All)

                
                exposure_time = cam.ExposureTime
                exposure_time.set(Exposure*1000)
                print(f"Exposure geändert:{(exposure_time.get()/1000):.0f}")
                
                frame = cam.get_frame(timeout_ms=5000).as_opencv_image()
                
        except Exception as e:
                    print(f"Fehler beim Abrufen des Frames: {e}")
                    frame = None
                    print(f"'Frame: {frame}'")
        return frame
        

def snap_image(Exposure):
    ordnerpfad = get_usb_path()
    image_file = f"Belichtungstest_{Exposure}_ms.jpg"
    dateipfad = os.path.join(ordnerpfad, image_file)

    dim_up()
    print("dimme LED hoch")
    frame = get_frame(Exposure)
    dim_down()
    print("dimme LED runter")

    try:
        cv2.imwrite(dateipfad, frame)
        print(f"Bild gespeichert: {dateipfad}")         

    except Exception as e:
        print(f"Fehler beim Speichern des Bildes: {e}")


if __name__ == "__main__":
    print("Starte Belichtungstest...")
    time.sleep(7 * 60 * 60)
    initial_exposure = 1  # Startwert für die Belichtungszeit in ms
    for exposure in range(initial_exposure, 1001, 10):  # Belichtungszeiten von 1 ms bis 1000 ms in Schritten von 10 ms
        print(f"Teste Belichtungszeit: {exposure} ms")
        snap_image(exposure)
        time.sleep(2)  # Kurze Pause zwischen den Aufnahmen