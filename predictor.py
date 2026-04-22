import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

def predict(history):
    if len(history) < 20:
        return None
    data = []
    for h in history:
        dt = h.timestamp
        data.append({
            'time': dt.timestamp(),
            'hour': dt.hour,
            'day': dt.timetuple().tm_yday,
            'humidity': h.humidity if h.humidity else 0,
            'wind': h.wind_speed if h.wind_speed else 0,
            'temp': h.temp
        })
    df = pd.DataFrame(data)
    X = df[['time', 'hour', 'day', 'humidity', 'wind']]
    y = df['temp']
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    last = history[-1]
    next_dt = last.timestamp + timedelta(hours=1)
    next_X = pd.DataFrame([{
        'time': next_dt.timestamp(),
        'hour': next_dt.hour,
        'day': next_dt.timetuple().tm_yday,
        'humidity': last.humidity if last.humidity else 0,
        'wind': last.wind_speed if last.wind_speed else 0
    }])
    val = rf.predict(next_X)[0]
    return {
        "temp": f"{round(val, 1)}°C",
        "time": next_dt.strftime('%H:%M')
    }

def analyze(history):
    if not history:
        return {"avg": 0, "status": "N/A"}
    temps = [h.temp for h in history]
    avg = sum(temps) / len(temps)
    status = "Stable"
    if len(temps) >= 2:
        if temps[-1] > temps[0]:
            status = "Increasing"
        elif temps[-1] < temps[0]:
            status = "Decreasing"
    return {
        "avg": round(avg, 1),
        "status": status
    }
