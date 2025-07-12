from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.reservation import Reservation, RoomPrice, Image
from functools import wraps
from datetime import datetime
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint("admin", __name__)

# Admin giriş kontrolü için decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Yönetim paneline erişmek için giriş yapmalısınız.', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Basit admin kontrolü (production'da daha güvenli olmalı)
        if username == "admin" and password == "otel123":
            session['admin_logged_in'] = True
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'danger')
    
    return render_template("admin_login.html")

@admin_bp.route("/logout")
def logout():
    session.pop('admin_logged_in', None)
    flash('Başarıyla çıkış yaptınız!', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route("/")
@admin_required
def dashboard():
    try:
        reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
        room_prices = RoomPrice.query.all()
        
        # Fotoğraf sayılarını al
        room_images_count = Image.query.filter_by(category='room').count()
        slider_images_count = Image.query.filter_by(category='slider').count()
        total_images_count = room_images_count + slider_images_count
        
        # Bu ay sayısını hesapla
        current_month = datetime.now().month
        current_month_count = sum(1 for r in reservations if r.created_at.month == current_month)
        
        return render_template("admin.html", 
                             reservations=reservations, 
                             current_month_count=current_month_count,
                             room_prices=room_prices,
                             room_images_count=room_images_count,
                             slider_images_count=slider_images_count,
                             total_images_count=total_images_count)
    except Exception as e:
        flash(f'Veritabanı hatası: {str(e)}', 'danger')
        return render_template("admin.html", 
                             reservations=[], 
                             current_month_count=0,
                             room_prices=[],
                             room_images_count=0,
                             slider_images_count=0,
                             total_images_count=0)

@admin_bp.route("/prices")
@admin_required
def manage_prices():
    try:
        room_prices = RoomPrice.query.all()
        return render_template("admin_prices.html", room_prices=room_prices)
    except Exception as e:
        flash(f'Fiyat yönetimi hatası: {str(e)}', 'danger')
        return render_template("admin_prices.html", room_prices=[])

@admin_bp.route("/prices/update", methods=["POST"])
@admin_required
def update_price():
    room_type = request.form.get("room_type")
    price = request.form.get("price")
    description = request.form.get("description")
    is_discounted = request.form.get("is_discounted") == "on"
    discount_percentage = float(request.form.get("discount_percentage", 0))
    
    room_price = RoomPrice.query.filter_by(room_type=room_type).first()
    if room_price:
        # Eğer orijinal fiyat henüz set edilmemişse, mevcut fiyatı orijinal fiyat olarak kullan
        if not hasattr(room_price, 'original_price') or room_price.original_price is None:
            room_price.original_price = room_price.price_per_night
        
        # İndirim aktifse, yeni fiyatı hesapla
        if is_discounted and discount_percentage > 0:
            room_price.original_price = float(price)  # Kullanıcının girdiği fiyat orijinal fiyat
            room_price.price_per_night = room_price.get_discounted_price()
        else:
            room_price.original_price = float(price)
            room_price.price_per_night = float(price)
        
        room_price.description = description
        room_price.is_discounted = is_discounted
        room_price.discount_percentage = discount_percentage
    else:
        # Yeni oda fiyatı oluştur
        original_price = float(price)
        if is_discounted and discount_percentage > 0:
            discounted_price = original_price * (1 - discount_percentage / 100)
        else:
            discounted_price = original_price
        
        room_price = RoomPrice(
            room_type=room_type,
            price_per_night=discounted_price,
            original_price=original_price,
            description=description,
            is_discounted=is_discounted,
            discount_percentage=discount_percentage
        )
        from app import db
        db.session.add(room_price)
    
    from app import db
    db.session.commit()
    
    if is_discounted and discount_percentage > 0:
        flash(f'{room_type} oda fiyatı %{discount_percentage} indirimle güncellendi!', 'success')
    else:
        flash(f'{room_type} oda fiyatı güncellendi!', 'success')
    
    return redirect(url_for('admin.manage_prices'))

@admin_bp.route("/images")
@admin_required
def manage_images():
    try:
        room_images = Image.query.filter_by(category='room').order_by(Image.room_type, Image.display_order).all()
        slider_images = Image.query.filter_by(category='slider').order_by(Image.display_order).all()
        return render_template("admin_images.html", room_images=room_images, slider_images=slider_images)
    except Exception as e:
        flash(f'Fotoğraf yönetimi hatası: {str(e)}', 'danger')
        return render_template("admin_images.html", room_images=[], slider_images=[])

@admin_bp.route("/images/upload", methods=["POST"])
@admin_required
def upload_image():
    if 'image' not in request.files:
        flash('Dosya seçilmedi!', 'danger')
        return redirect(url_for('admin.manage_images'))
    
    file = request.files['image']
    category = request.form.get("category")
    room_type = request.form.get("room_type", "")
    
    if file.filename == '':
        flash('Dosya seçilmedi!', 'danger')
        return redirect(url_for('admin.manage_images'))
    
    if file:
        filename = secure_filename(file.filename)
        # Dosyayı kaydet
        upload_folder = f'app/static/images/{category}'
        if category == 'room' and room_type:
            upload_folder = f'app/static/images/{room_type.lower()}'
        elif category == 'slider':
            upload_folder = 'app/static/images'
        
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Veritabanına kaydet
        image = Image(
            filename=filename,
            category=category,
            room_type=room_type if room_type else None,
            display_order=Image.query.filter_by(category=category).count() + 1
        )
        from app import db
        db.session.add(image)
        db.session.commit()
        
        flash('Fotoğraf başarıyla yüklendi!', 'success')
    
    return redirect(url_for('admin.manage_images'))

@admin_bp.route("/images/delete/<int:image_id>", methods=["POST"])
@admin_required
def delete_image(image_id):
    try:
        image = Image.query.get_or_404(image_id)
        filename = image.filename
        
        # Dosya yolunu belirle
        if image.category == 'room' and image.room_type:
            file_path = os.path.join('app', 'static', 'images', image.room_type.lower(), filename)
        else:
            file_path = os.path.join('app', 'static', 'images', filename)
        
        # Dosyayı sil
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                flash(f'"{filename}" dosyası başarıyla silindi!', 'success')
            except OSError as e:
                flash(f'Dosya silinirken hata oluştu: {str(e)}', 'danger')
                return redirect(url_for('admin.manage_images'))
        else:
            flash(f'"{filename}" dosyası bulunamadı, ancak veritabanından silindi.', 'warning')
        
        # Veritabanından sil
        from app import db
        db.session.delete(image)
        db.session.commit()
        
        flash(f'"{filename}" fotoğrafı başarıyla silindi!', 'success')
        
    except Exception as e:
        flash(f'Fotoğraf silinirken hata oluştu: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_images'))
