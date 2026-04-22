from flask import Flask, render_template, request, jsonify
from database import db, WeatherHistory
from api_client import fetch, archive
from predictor import predict, analyze
import os
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///weather.db')

db.init_app(app)

with app.app_context():
    db.create_all()

def icon(code):
    m = {
        0: "01d", 1: "01d", 2: "02d", 3: "03d",
        45: "50d", 48: "50d",
        51: "09d", 53: "09d", 55: "09d",
        61: "10d", 63: "10d", 65: "10d",
        80: "10d", 81: "10d", 82: "10d",
        95: "11d", 96: "11d", 99: "11d"
    }
    return m.get(code, "03d")

def chart(history):
    if not history: return None
    history.sort(key=lambda x: x.timestamp)
    x = [h.timestamp.strftime('%m-%d %H:%M') for h in history]
    y = [h.temp for h in history]
    plt.figure(figsize=(15, 5)) 
    plt.plot(x, y, marker='o', markersize=3, linestyle='-', color='#3498db', linewidth=1.5)
    plt.title('History Chart (Last 7 Days)', fontsize=14, pad=15)
    plt.ylabel('Temp (°C)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.4)
    ax = plt.gca()
    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        if i % 12 != 0: label.set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    plt.close() 
    return f"data:image/png;base64,{img}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather', methods=['POST'])
def info():
    city = request.json.get('city')
    if not city: return jsonify({'error': 'Missing City'}), 400
    count = WeatherHistory.query.filter_by(city=city).count()
    fresh = count == 0
    weather = fetch(city)
    if not weather: return jsonify({'error': 'Fetch Error'}), 500
    sync = []
    if fresh:
        sync = archive(weather['lat'], weather['lon'])
        for p in sync:
            ts = datetime.fromisoformat(p['time'])
            db.session.add(WeatherHistory(
                city=weather['city'], temp=p['temp'],
                humidity=p.get('humidity', 0), pressure=0, 
                wind_speed=p.get('wind_speed', 0),
                description="Archive", icon="01d", timestamp=ts
            ))
        db.session.commit()
    
    for p in weather['past']:
        ts = datetime.fromisoformat(p['time'])
        exists = WeatherHistory.query.filter_by(city=weather['city'], timestamp=ts).first()
        if not exists:
            db.session.add(WeatherHistory(
                city=weather['city'], temp=p['temp'],
                humidity=p.get('humidity', 0), pressure=0, 
                wind_speed=p.get('wind_speed', 0),
                description="Live", icon="01d", timestamp=ts
            ))
    db.session.commit()
    
    now = datetime.now()
    history = WeatherHistory.query.filter(
        WeatherHistory.city == weather['city'],
        WeatherHistory.timestamp <= now
    ).order_by(WeatherHistory.timestamp.asc()).all()
    
    points = history[-168:] if len(history) > 168 else history
    pred = predict(history)
    stats = analyze(history)
    plot = chart(points)

    weather['icon'] = icon(weather['code'])
    forecast = []
    for f in weather['today']:
        ts = datetime.fromisoformat(f['time'])
        forecast.append({
            'time': ts.strftime('%H:%M'), 
            'temp': f['temp'], 
            'icon': icon(f['code'])
        })
    
    return jsonify({
        'current': weather,
        'history': [h.to_dict() for h in history],
        'forecast': forecast,
        'prediction': pred,
        'trends': stats,
        'chart_url': plot
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
