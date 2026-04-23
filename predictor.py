import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
def predict(history):
    if not history:return {"temp":0,"time":"No data"}
    data=[]
    for h in history:
        data.append({'timestamp':h.timestamp,'temp':h.temp,'humidity':h.humidity,'wind_speed':h.wind_speed,'pressure':h.pressure})
    df=pd.DataFrame(data)
    df['ts']=pd.to_datetime(df['timestamp']).astype(int)/10**9
    df['hour']=pd.to_datetime(df['timestamp']).dt.hour
    df['day']=pd.to_datetime(df['timestamp']).dt.dayofyear
    X=df[['ts','hour','day','humidity','wind_speed','pressure']]
    y=df['temp']
    model=RandomForestRegressor(n_estimators=100,random_state=42)
    model.fit(X,y)
    now=datetime.now()
    last=df.iloc[-1]
    future_X=pd.DataFrame([[now.timestamp(),now.hour,now.timetuple().tm_yday,last['humidity'],last['wind_speed'],last['pressure']]],columns=['ts','hour','day','humidity','wind_speed','pressure'])
    p=model.predict(future_X)[0]
    return {"temp":round(p,1),"time":now.strftime("%H:00")}
def analyze(history):
    if not history:return {"avg":0}
    temps=[h.temp for h in history[-744:]]
    if not temps:return {"avg":0}
    avg=sum(temps)/len(temps)
    return {"avg":round(avg,1)}
