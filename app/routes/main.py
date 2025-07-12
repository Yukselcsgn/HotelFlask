from flask import Blueprint, render_template
from app.models.reservation import RoomPrice

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

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
