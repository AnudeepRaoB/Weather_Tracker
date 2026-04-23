from flask import Flask,render_template,request,jsonify
from database import db,WeatherHistory
from api_client import fetch,archive
from predictor import predict,analyze
import os
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io,base64,matplotlib
matplotlib.use('Agg')
load_dotenv()
app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']=os.getenv('FLASK_SECRET_KEY','default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL','sqlite:///weather.db')
db.init_app(app)
with app.app_context():
    db.create_all()
def icon(c,day=1):
    res="02d"
    if c<=3:res=["01d","01d","02d","03d"][c]
    elif c<=9 or 10<=c<=12 or 30<=c<=39 or 40<=c<=49:res="50d"
    elif 20<=c<=29 or 50<=c<=59 or (80<=c<=90 and c not in[85,86]):res="09d"
    elif 60<=c<=69:res="10d"
    elif 70<=c<=79 or c in[85,86]:res="13d"
    elif 91<=c<=99:res="11d"
    return res if day else res.replace('d', 'n')
def chart(history):
    if not history:return None
    history.sort(key=lambda x:x.timestamp)
    x=[h.timestamp.strftime('%m-%d %H:%M') for h in history]
    y=[h.temp for h in history]
    plt.figure(figsize=(15,5))
    plt.plot(x,y,marker='o',markersize=3,linestyle='-',color='#3498db',linewidth=1.5)
    plt.title('History Chart',fontsize=14,pad=15)
    plt.ylabel('Temp (°C)',fontsize=12)
    plt.grid(True,linestyle='--',alpha=0.4)
    ax=plt.gca()
    for i,label in enumerate(ax.xaxis.get_ticklabels()):
        if i%12!=0:label.set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf=io.BytesIO()
    plt.savefig(buf,format='png',dpi=100)
    buf.seek(0)
    img=base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f"data:image/png;base64,{img}"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/weather',methods=['POST'])
def info():
    city=request.json.get('city')
    if not city:return jsonify({'error':'Missing City'}),400
    count=WeatherHistory.query.filter_by(city=city).count()
    fresh=count==0
    weather=fetch(city)
    if not weather:return jsonify({'error':'Fetch Error'}),500
    if fresh:
        sync=archive(weather['lat'],weather['lon'])
        for p in sync:
            db.session.add(WeatherHistory(city=weather['city'],temp=p['temp'],humidity=p.get('humidity',0),pressure=p.get('pressure',0),wind_speed=p.get('wind_speed',0),description="Archive",icon=icon(p.get('code',0),p.get('is_day',1)),timestamp=datetime.fromisoformat(p['time'])))
        db.session.commit()
    for p in weather['past']:
        ts=datetime.fromisoformat(p['time'])
        exists=WeatherHistory.query.filter_by(city=weather['city'],timestamp=ts).first()
        if not exists:
             db.session.add(WeatherHistory(city=weather['city'],temp=p['temp'],humidity=p.get('humidity',0),pressure=p.get('pressure',0),wind_speed=p.get('wind_speed',0),description="Live",icon=icon(p.get('code',0),p.get('is_day',1)),timestamp=ts))
    db.session.commit()
    now=datetime.now()
    history=WeatherHistory.query.filter(WeatherHistory.city==weather['city'],WeatherHistory.timestamp<=now).order_by(WeatherHistory.timestamp.asc()).all()
    points=history[-168:] if len(history)>168 else history
    pred=predict(history)
    month=history[-744:] if len(history)>744 else history
    stats=analyze(month)
    plot=chart(points)
    weather['icon']=icon(weather['code'],weather['is_day'])
    forecast=[]
    for f in weather['today']:
        ts=datetime.fromisoformat(f['time'])
        forecast.append({'time':ts.strftime('%H:%M'),'temp':f['temp'],'icon':icon(f['code'],f['is_day'])})
    return jsonify({'current':weather,'forecast':forecast,'prediction':pred,'trends':stats,'chart_url':plot})
if __name__=='__main__':
    app.run(debug=True,port=5001)
