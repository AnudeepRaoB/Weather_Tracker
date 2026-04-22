from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WeatherHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    description = db.Column(db.String(200))
    icon = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'temp': self.temp,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'description': self.description,
            'icon': self.icon,
            'timestamp': self.timestamp.isoformat()
        }
