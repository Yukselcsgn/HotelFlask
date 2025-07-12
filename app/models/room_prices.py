from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RoomPrice(db.Model):
    __tablename__ = 'room_prices'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), nullable=False)
    original_price = db.Column(db.Float, nullable=True)
    discounted_price = db.Column(db.Float, nullable=True)
