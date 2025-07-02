import requests 
import urllib.parse 
import os
import time

geocode_url = "https://graphhopper.com/api/1/geocode?" 
route_url = "https://graphhopper.com/api/1/route?" 
key = "c22eab77-0c5e-4fad-93d9-1afec197d0a9"

def geocoding (location, key): 

    geocode_url = "https://graphhopper.com/api/1/geocode?"  
    
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key}) 
    replydata = requests.get(url) 
    json_data = replydata.json() 
    json_status = replydata.status_code 
    if json_status == 200 and len(json_data["hits"]) !=0: 
        json_data = requests.get(url).json() 
        lat=(json_data["hits"][0]["point"]["lat"]) 
        lng=(json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        if "country" in json_data["hits"][0]: 
            country = json_data["hits"][0]["country"] 
        else: 
            country="" 
        if "state" in json_data["hits"][0]: 
            state = json_data["hits"][0]["state"] 
        else: 
            state="" 
        if len(state) !=0 and len(country) !=0: 
            new_loc = name + ", " + state + ", " + country 
        elif len(state) !=0: 
            new_loc = name + ", " + country 
    else: 
        lat="null" 
        lng="null" 
        new_loc=location
    return json_status,lat,lng,new_loc


while True: 
    print("=================================================")
    print("Mida la Distancia entre una Ciudad de Chile y una Ciudad de Argentina")
    chile = "santiago chile"
    argentina = "mendoza argentina"
    ciudadchile = geocoding(chile, key)
    ciudadargentina = geocoding(argentina, key)
    print("=================================================")

    if ciudadchile[0] == 200 and ciudadargentina[0] == 200: 
        iniciochile="&point="+str(ciudadchile[1])+"%2C"+str(ciudadchile[2]) 
        destinoargentina="&point="+str(ciudadargentina[1])+"%2C"+str(ciudadargentina[2]) 
        paths_url = route_url + urllib.parse.urlencode({"key":key}) + iniciochile + destinoargentina
        paths_status = requests.get(paths_url).status_code 
        paths_data = requests.get(paths_url).json()
        if paths_status == 200: 
            kilometrosentreciudades = (paths_data["paths"][0]["distance"])/1000 
            print("Distancia entre {1} y {2} : {0:.0f} km".format(kilometrosentreciudades, chile, argentina)) 
            print("=================================================")

    ciudad_origen = input("Ingresa Ciudad de Origen: ")
    ciudad_destino = input("Ingresa Ciudad de destino: ")
    print("1.Auto / 2.A Pie / 3.Moto / 4.Camion")
    seleccionavehiculo = int(input("Ingresa un tipo de vehiculo para el calculo: "))
    if seleccionavehiculo == 1:
        vehiculo = str("car")
    if seleccionavehiculo == 2:
        vehiculo = str("foot")
    if seleccionavehiculo == 3:
        vehiculo = str("motorcycle")
    if seleccionavehiculo == 4:
        vehiculo = str("truck")

    ciudaddeorigen = geocoding(ciudad_origen, key)
    ciudaddedestino = geocoding(ciudad_destino, key)


    if ciudaddeorigen[0] == 200 and ciudaddedestino[0] == 200:
        op="&point="+str(ciudaddeorigen[1])+"%2C"+str(ciudaddeorigen[2]) 
        dp="&point="+str(ciudaddedestino[1])+"%2C"+str(ciudaddedestino[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key}) + op + dp + "&vehicle=" + vehiculo
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

    print("=================================================") 
    print("Distancia desde " + ciudad_origen + " hasta " + ciudad_destino) 
    print("=================================================") 
    if paths_status == 200: 
        miles = (paths_data["paths"][0]["distance"])/1000/1.61 
        km = (paths_data["paths"][0]["distance"])/1000 
        sec = int(paths_data["paths"][0]["time"]/1000%60) 
        min = int(paths_data["paths"][0]["time"]/1000/60%60) 
        hr = int(paths_data["paths"][0]["time"]/1000/60/60) 
        print("Distancia Recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km)) 
        print("Duracion del Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
        print("=================================================")

        for each in range(len(paths_data["paths"][0]["instructions"])): 
            path = paths_data["paths"][0]["instructions"][each]["text"] 
            distance = paths_data["paths"][0]["instructions"][each]["distance"] 
            print("{0} ( {1:.1f} km / {2:.1f} millas )".format(path, distance/1000, distance/1000/1.61)) 
            print("=============================================") 

        salir = input(str("Ingresa una s para salir: "))
        if salir == "s":
            break
    print("Espera de 60 si no Graphhopper no respondera")
    time.sleep(60)