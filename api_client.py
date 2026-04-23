import requests
from datetime import datetime,timedelta
GEO="https://geocoding-api.open-meteo.com/v1/search"
WEATHER="https://api.open-meteo.com/v1/forecast"
ARCHIVE="https://archive-api.open-meteo.com/v1/archive"
def locate(city):
    params={"name":city,"count":1,"language":"en","format":"json"}
    try:
        res=requests.get(GEO,params=params)
        res.raise_for_status()
        data=res.json()
        if "results" in data:
            res=data["results"][0]
            return {"lat":res["latitude"],"lon":res["longitude"],"name":res["name"]}
    except:pass
    return None
def archive(lat,lon):
    end=(datetime.now()-timedelta(days=2)).strftime('%Y-%m-%d')
    start=(datetime.now()-timedelta(days=5*365)).strftime('%Y-%m-%d')
    params={"latitude":lat,"longitude":lon,"start_date":start,"end_date":end,"hourly":["temperature_2m","relative_humidity_2m","wind_speed_10m","weather_code","surface_pressure"],"timezone":"auto"}
    try:
        res=requests.get(ARCHIVE,params=params)
        res.raise_for_status()
        data=res.json()
        h=data["hourly"]
        points=[]
        for i in range(0,len(h["time"]),6):
            hr=datetime.fromisoformat(h["time"][i]).hour
            is_day=1 if 6<=hr<=18 else 0
            points.append({"time":h["time"][i],"temp":h["temperature_2m"][i],"humidity":h["relative_humidity_2m"][i],"wind_speed":h["wind_speed_10m"][i],"code":h["weather_code"][i],"pressure":h["surface_pressure"][i],"is_day":is_day})
        return points
    except:return []
def fetch(city):
    geo=locate(city)
    if not geo:return None
    params={"latitude":geo["lat"],"longitude":geo["lon"],"current":["temperature_2m","relative_humidity_2m","surface_pressure","wind_speed_10m","weather_code","is_day"],"hourly":["temperature_2m","relative_humidity_2m","surface_pressure","wind_speed_10m","weather_code","is_day"],"past_days":31,"forecast_days":1,"timezone":"auto"}
    try:
        res=requests.get(WEATHER,params=params)
        data=res.json()
        h=data["hourly"]
        past,today=[],[]
        city_now=datetime.fromisoformat(data["current"]["time"])
        city_today=city_now.strftime('%Y-%m-%d')
        for i in range(len(h["time"])):
            ts=datetime.fromisoformat(h["time"][i])
            point={"time":h["time"][i],"temp":h["temperature_2m"][i],"humidity":h["relative_humidity_2m"][i],"wind_speed":h["wind_speed_10m"][i],"code":h["weather_code"][i],"pressure":h["surface_pressure"][i],"is_day":h["is_day"][i]}
            if ts<=city_now:past.append(point)
            if ts.strftime('%Y-%m-%d')==city_today:today.append(point)
        return {"city":geo["name"],"lat":geo["lat"],"lon":geo["lon"],"temp":data["current"]["temperature_2m"],"humidity":data["current"]["relative_humidity_2m"],"pressure":data["current"]["surface_pressure"],"wind_speed":data["current"]["wind_speed_10m"],"is_day":data["current"]["is_day"],"description":"Code: "+str(data["current"]["weather_code"]),"code":data["current"]["weather_code"],"past":past,"today":today}
    except:return None
