from GPIO_Setup import button_pressed
from OLED_panel import display_text
import json
import time
from json_read_write import *
from log import log_schreiben

with open("/home/Ento/LepmonOS/sites.json", "r") as f:
    data = json.load(f)





def set_location_code():
    country_old = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "locality", "country")
    province_old = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "locality", "province")
    city_code_old = get_value_from_section("/home/Ento/LepmonOS/Lepmon_config.json", "locality", "city")
    level = "country"
    index = 0
    country = None
    province = None
    city_code = None
    while True:
        if level == "country":
            countries = list(data.keys())
            display_text("Bitte Land wählen:",f"{countries[index]}","")
        elif level == "province":
            provinces = list(data[country].keys())
            display_text("Bitte Provinz wählen:", provinces[index],"")
        elif level == "city":
            codes = data[country][province]
            display_text("Stadt wählen:", codes[index],"")

        if button_pressed("oben"):
            if level == "country":
                index = (index - 1) % len(data)
            elif level == "province":
                index = (index - 1) % len(data[country])
            elif level == "city":
                city_count = len(data[country][province])
                if city_count >1:
                    index = (index - 1) % city_count
                    index = max(1, index)

        if button_pressed("unten"):
            if level == "country":
                index = (index + 1) % len(data)
            elif level == "province":
                index = (index + 1) % len(data[country])       
            elif level == "city":
                city_count = len(data[country][province])
                if city_count >1:
                    index = (index + 1) % city_count
                    index = max(1, index)     
        if button_pressed("rechts"):
            if level == "country":
                country = countries[index]
                level = "province"
                index = 0
            elif level == "province":
                provinces = list(data[country].keys())
                province = provinces[index]
                print(province)
                codes = data[country][province]
                province_code = codes[0] if codes else None
                print(province_code)
                level = "city"
                city_count = len(data[country][province])
                index = 1 if city_count > 1 else 0
            elif level == "city":
                codes = data[country][province]
                city_code = codes[index]
        if button_pressed("enter"):
            display_text("Auswahl abgeschlossen","","")
            print(f"Ausgewählter Ort: {country} {province_code} {city_code}")
            time.sleep(3)
            display_text(f"{country}",f"{province}", f"{city_code}")
            time.sleep(3)
            break
        time.sleep(.05)
        
    
    
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "locality", "country", country)   
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "locality", "province",province_code)
    write_value_to_section("/home/Ento/LepmonOS/Lepmon_config.json", "locality", "city",city_code)
    print("saved information on location code in configuration file")
        
    new = False
        
    if country == country_old:
        log_schreiben(f"Land unverändert: {country}")
    elif country != country_old:
        log_schreiben(f"Land wurde neu eingegeben: {country}")
        new = True
        
    if province_code == province_old:
        log_schreiben(f"Provinz unverändert: {province}")
    elif province_code != province_old:
        log_schreiben(f"Provinz wurde neu eingegeben: {province}")
        new = True
        
    if city_code == city_code_old:
        log_schreiben(f"Stadt unverändert: {city_code}")
    elif city_code != city_code_old:
        log_schreiben(f"Stadt wurde neu eingegeben: {city_code}")
        new = True
            
    return new

if __name__ == "__main__":
    set_location_code()


            
           
