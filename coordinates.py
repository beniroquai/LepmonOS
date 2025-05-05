from GPIO_Setup import turn_on_led, turn_off_led, button_pressed
from OLED_panel import display_text
from json_read_write import *
import time
from service import log_schreiben
from error_handling import error_message


def coordinates_in_list(latitude,longitude):
  
  if latitude / 10 < 1:
    latitude_str = str(latitude).replace('.', '')
    latitude_str = str(0)+latitude_str
  
  elif latitude / 10 >= 1:
    latitude_str = str(latitude).replace('.', '')
    
  fehlende_nullen = 9 - len(latitude_str)
  if fehlende_nullen > 0:
      latitude_str = latitude_str + '0' * fehlende_nullen
  
  latitude_list = [int(x) for x in latitude_str]


  if 0.1 > longitude / 100 >= 0.01:
    longitude_str = str(longitude).replace('.', '')
    longitude_str = str(0)+str(0)+longitude_str  
    
  elif 1 > longitude / 100 >= 0.1:
    longitude_str = str(longitude).replace('.', '')
    longitude_str = str(0)+longitude_str
    
  elif longitude / 100 >= 1:
    longitude_str = str(longitude).replace('.', '')

  fehlende_nullen = 10 - len(longitude_str)
  if fehlende_nullen > 0:
      longitude_str = longitude_str + '0' * fehlende_nullen

  longitude_list = [int(x) for x in longitude_str]


  return latitude_list, longitude_list



def set_coordinates():
    try:
        latitude_read, longitude_read, pol, block = (get_coordinates())
    except Exception as e:
        error_message(11,e)    
    log_schreiben(f"alte Koordinaten: Breite {latitude_read}, Länge {latitude_read}")
    print(f"Breite:{latitude_read}")
    print(f"Länge:{longitude_read}")
    display_text("Bitte","Hemisphaeren","eingeben")
    time.sleep(3)
    display_text("Knopf oben = Nord","","Knopf unten = Süd")

    user = False
    nordsued = ""
    while not user:
        turn_on_led("blau")
        if button_pressed("oben"):
            nordsued ="N"
            user = True
            turn_off_led("blau")
        if button_pressed("unten"):
            nordsued ="S"
            user = True
            turn_off_led("blau")
        else:
            time.sleep(.05)   

    display_text("Knopf oben = Ost","","Knopf unten = West")
    user = False
    eastwest = ""
    while not user:
        turn_on_led("blau")
        if button_pressed("oben"):
            eastwest ="E"
            user = True
            turn_off_led("blau")
        if button_pressed("unten"):
            eastwest ="W"
            user = True
            turn_off_led("blau")
        else:
            time.sleep(.05)  

    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "GPS", "Pol",nordsued)     
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "GPS", "Block",eastwest) 
    print("saved information on hemisphere in configuration file")


    latitude_list, longitude_list = coordinates_in_list(latitude_read, longitude_read)

    aktuelle_position = 0
    Wahlmodus = 1
    while True:
      turn_on_led("blau")
      if Wahlmodus == 1 :
        if aktuelle_position < 2:
          positionszeiger = pol+"_" * aktuelle_position
        else:
          positionszeiger =  pol+"__." +"_" * (aktuelle_position -2)  
        positionszeiger += "x"  
        display_text("Latitude eingeben",
                    f"{pol}{latitude_list[0]}{latitude_list[1]}.{latitude_list[2]}{latitude_list[3]}{latitude_list[4]}{latitude_list[5]}{latitude_list[6]}{latitude_list[7]}{latitude_list[8]}",
                    positionszeiger)
        
      if Wahlmodus == 2 :
        if aktuelle_position < 3:
          positionszeiger = block + "_" * aktuelle_position
        else:
          positionszeiger = block + "___." + "_" * (aktuelle_position -3)
        positionszeiger += "x"  
        display_text("Longitude eingeben",
                     f"{block}{longitude_list[0]}{longitude_list[1]}{longitude_list[2]}.{longitude_list[3]}{longitude_list[4]}{longitude_list[5]}{longitude_list[6]}{longitude_list[7]}{longitude_list[8]}{longitude_list[9]}",
                     positionszeiger)
        

      if button_pressed("oben"):
        if Wahlmodus == 1 :
          latitude_list[aktuelle_position] = (latitude_list[aktuelle_position] + 1) % 10

        if Wahlmodus == 2 :
          longitude_list[aktuelle_position] = (longitude_list[aktuelle_position] + 1) % 10  

      if button_pressed("unten"):
        if Wahlmodus == 1 :
          latitude_list[aktuelle_position] = (latitude_list[aktuelle_position] - 1) % 10

        if Wahlmodus == 2 :
          longitude_list[aktuelle_position] = (longitude_list[aktuelle_position] - 1) % 10      

      if button_pressed("rechts"):
        if Wahlmodus == 1 :
          aktuelle_position = (aktuelle_position + 1) % 9
          aktuelle_position = aktuelle_position
        if Wahlmodus == 2 :
          aktuelle_position = (aktuelle_position + 1) % 10
          aktuelle_position = aktuelle_position  


      if button_pressed("enter"):
        Wahlmodus +=1
        aktuelle_position = 0 
      
      if Wahlmodus == 3 :
        turn_off_led("blau")
        break  
      time.sleep(0.05)

    latitude_write = float(f"{latitude_list[0]}{latitude_list[1]}.{latitude_list[2]}{latitude_list[3]}{latitude_list[4]}{latitude_list[5]}{latitude_list[6]}{latitude_list[7]}{latitude_list[8]}")
    longitude_write = float(f"{longitude_list[0]}{longitude_list[1]}{longitude_list[2]}.{longitude_list[3]}{longitude_list[4]}{longitude_list[5]}{longitude_list[6]}{longitude_list[7]}{longitude_list[8]}{longitude_list[9]}")

    print(f"Breite_alt:{latitude_read}")
    print(f"Breite_neu:{latitude_write}")    

    print(f"Länge_alt:{longitude_read}")
    print(f"Länge_neu:{longitude_write}")    


    if latitude_write == latitude_read:
      print("Breite unverändert")
      log_schreiben(f"Breite unverändert")
    if longitude_write == longitude_read:
      print("Länge unverändert")     
      log_schreiben(f"Länge unverändert") 

# Prüfen, ob sich die Koordinaten geändert haben
    if latitude_write != latitude_read or longitude_write != longitude_read:
        log_schreiben(f"neue Koordinaten: Breite {latitude_write}, Länge {longitude_write}")
        write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "GPS", "latitude", latitude_write)     
        write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "GPS", "longitude", longitude_write)

        log_schreiben(f"neue Koordinaten wurden gespeichert")
        print("saved GPS coordinates in configuration file")

                










if __name__ == "__main__":
    set_coordinates()
    print("set coordinates")