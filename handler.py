import requests
import cache
import os
from dotenv import load_dotenv
load_dotenv()

weather_url = "http://api.weatherapi.com/v1"
# THE API KEY IS HIDDEN 
weatherapi_key = os.environ["weather"]
def current(location:str) -> dict:
    method = "current"
    r = cache.get(method, location)
    s = 200
    if not r:
        print("requesting")
        response = requests.get(f"{weather_url}/{method}.json?key={weatherapi_key}&q={location}")
        r = response.json()
        cache.store(method, location, r)
        s = response.status_code
    if 200 <= s <= 299:
        place = r['location']
        now = r['current']
        cw= {"temp": {"Cel":f"{now['temp_c']}°C", "Fah":f"{now['temp_f']}°F"},
        'cond':f"\n{now['condition']['text']} ",
        'icon':'https://'+now['condition']['icon'][2:]
        }
        cw['wind'] = ""  
        if now['wind_kph'] > 15: 
            cw['wind'] = f"\nwind speed: {now['wind_kph']} kpmh"
        
        cw['precip'] = ''
        if now['precip_mm'] > 0:
            cw['precip'] = f"\namount of rain: {now['precip_mm']}mm"
        
        cw['humidity'] = f"\nhumidity: {now['humidity']}%"
       
        cw['cloud'] = f"\ncloudiness: {now['cloud']}%"
            
        cw['colour'] = 'red' if now['temp_c'] > 30 else 'blue' if now['temp_c'] < 10 else 'green'
        cw['time'] = f"Currently in {place['name']}, {place['region']}, {place['country']}"
            
        cw['utime'] = f"\nlast updated at: `{now['last_updated']}`"

        print(f"""{"-"*35}\n{cw['time']}{cw['cond']}{"\nTemperature: "+cw['temp']['Cel']}{cw['wind']}{cw['precip']}{cw['humidity']}{cw['cloud']}{cw['utime']}\n{"-"*35}""")
    else:
        print( {'Error': r['error']['message']})


def forecast(location: str):
    method = "forecast"
    days = 2

    r = cache.get(method, location)
    s = 200

    if not r:
        print("requesting")
        response = requests.get(
            f"{weather_url}/{method}.json"
            f"?key={weatherapi_key}&q={location}&days={days}"
        )
        r = response.json()
        cache.store(method, location, r)
        s = response.status_code

    if 200 <= s <= 299:
        place = r["location"]
        forecasts = r["forecast"]["forecastday"]

        print("-" * 40)
        print(f"Forecast for {place['name']}, {place['region']}, {place['country']}")
        print("-" * 40)

        labels = ["Today", "Tomorrow"]

        for i, f in enumerate(forecasts):
            day = f["day"]
            label = labels[i] if i < len(labels) else f"Day {i+1}"

            print(f"\n==={label} ({f['date']})===")
            print(f"Condition: {day['condition']['text']}")
            print(f"Max Temp: {day['maxtemp_c']}°C")
            print(f"Min Temp: {day['mintemp_c']}°C")
            print(f"Chance of Rain: {day['daily_chance_of_rain']}%")
            print(f"Humidity: {day['avghumidity']}%")
        
        print("-" * 40)

    else:
        print({"Error": r.get("error", {}).get("message", "Unknown error")})



