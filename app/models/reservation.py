from app import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)  # Telefon numarası eklendi
    room_type = db.Column(db.String(80), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Reservation {self.name} - {self.room_type}>"

class RoomPrice(db.Model):
    __tablename__ = 'room_prices'

    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(80), unique=True, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=False)  # Orijinal fiyat
    discount_percentage = db.Column(db.Float, default=0.0)  # İndirim yüzdesi
    is_discounted = db.Column(db.Boolean, default=False)  # İndirim aktif mi?
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_discounted_price(self):
        """İndirimli fiyatı hesapla"""
        if self.is_discounted and self.discount_percentage > 0:
            return self.original_price * (1 - self.discount_percentage / 100)
        return self.original_price

    def __repr__(self):
        return f"<RoomPrice {self.room_type} - {self.price_per_night}TL>"

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'room', 'slider', 'gallery'
    room_type = db.Column(db.String(80))  # room kategorisi için
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Image {self.filename} - {self.category}>"

class FAQ(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FAQ {self.question[:50]}...>"
