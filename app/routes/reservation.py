from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.reservation import Reservation, RoomPrice
from datetime import datetime
from app.services.email_service import send_reservation_email, notify_owner_about_reservation

reservation_bp = Blueprint("reservation", __name__)

@reservation_bp.route("/", methods=["GET", "POST"])
def reserve():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            room_type = request.form.get("room_type")
            check_in = datetime.strptime(request.form.get("check_in"), "%Y-%m-%d").date()
            check_out = datetime.strptime(request.form.get("check_out"), "%Y-%m-%d").date()
            # Sabit otel sahibi e-postası
            owner_email = "altunpansiyon@gmail.com"

            if check_out <= check_in:
                flash("Çıkış tarihi giriş tarihinden sonra olmalıdır.", "danger")
                return redirect(url_for("reservation.reserve"))

            reservation = Reservation(
                name=name,
                email=email,
                room_type=room_type,
                check_in=check_in,
                check_out=check_out
            )
            db.session.add(reservation)
            db.session.commit()

            send_reservation_email(
                to_email=email,
                reservation_data={
                    "name": name,
                    "room_type": room_type,
                    "check_in": check_in.strftime("%d.%m.%Y"),
                    "check_out": check_out.strftime("%d.%m.%Y")
                }
            )

            notify_owner_about_reservation(
                reservation_data={
                    "name": name,
                    "email": email,
                    "room_type": room_type,
                    "check_in": check_in.strftime("%d.%m.%Y"),
                    "check_out": check_out.strftime("%d.%m.%Y")
                },
                owner_email=owner_email
            )

            flash("Rezervasyon başarıyla alındı.", "success")
            return redirect(url_for("reservation.success"))

        except Exception as e:
            flash(f"Hata oluştu: {str(e)}", "danger")

    try:
        room_prices = RoomPrice.query.all()
        # Create a dictionary for easy access
        prices_dict = {price.room_type: price for price in room_prices}
        return render_template("reserve.html", room_prices=prices_dict)
    except Exception as e:
        # If there's an error, pass empty dict
        return render_template("reserve.html", room_prices={})

@reservation_bp.route("/success")
def success():
    return render_template("success.html")

