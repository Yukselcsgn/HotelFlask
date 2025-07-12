from flask import Blueprint, render_template
from app.models.reservation import RoomPrice, FAQ, Image

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    try:
        # Aktif FAQ'ları getir
        faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.display_order, FAQ.created_at).all()
        
        # Aktif slider fotoğraflarını getir
        slider_images = Image.query.filter_by(category='slider', is_active=True).order_by(Image.display_order).all()
        
        return render_template("index.html", faqs=faqs, slider_images=slider_images)
    except Exception as e:
        # Hata durumunda boş liste ile devam et
        return render_template("index.html", faqs=[], slider_images=[])

@main_bp.route("/rooms")
def rooms():
    try:
        room_prices = RoomPrice.query.all()
        # Create a dictionary for easy access
        prices_dict = {price.room_type: price for price in room_prices}
        return render_template("rooms.html", room_prices=prices_dict)
    except Exception as e:
        # If there's an error, pass empty dict
        return render_template("rooms.html", room_prices={})
