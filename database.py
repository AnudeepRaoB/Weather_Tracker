from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy()
class WeatherHistory(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    city=db.Column(db.String(100),nullable=False)
    temp=db.Column(db.Float,nullable=False)
    humidity=db.Column(db.Float,nullable=False)
    pressure=db.Column(db.Float,nullable=False)
    wind_speed=db.Column(db.Float,nullable=False)
    description=db.Column(db.String(100),nullable=False)
    icon=db.Column(db.String(20),nullable=False)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
