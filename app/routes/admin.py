from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.reservation import Reservation, RoomPrice, Image, FAQ
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

# FAQ Yönetimi
@admin_bp.route("/faq")
@admin_required
def manage_faq():
    try:
        faqs = FAQ.query.order_by(FAQ.display_order, FAQ.created_at).all()
        return render_template("admin_faq.html", faqs=faqs)
    except Exception as e:
        flash(f'FAQ yönetimi hatası: {str(e)}', 'danger')
        return render_template("admin_faq.html", faqs=[])

@admin_bp.route("/faq/add", methods=["POST"])
@admin_required
def add_faq():
    question = request.form.get("question")
    answer = request.form.get("answer")
    display_order = int(request.form.get("display_order", 0))
    
    if not question or not answer:
        flash('Soru ve cevap alanları zorunludur!', 'danger')
        return redirect(url_for('admin.manage_faq'))
    
    faq = FAQ(
        question=question,
        answer=answer,
        display_order=display_order
    )
    
    from app import db
    db.session.add(faq)
    db.session.commit()
    
    flash('FAQ başarıyla eklendi!', 'success')
    return redirect(url_for('admin.manage_faq'))

@admin_bp.route("/faq/edit/<int:faq_id>", methods=["POST"])
@admin_required
def edit_faq(faq_id):
    try:
        faq = FAQ.query.get_or_404(faq_id)
        faq.question = request.form.get("question")
        faq.answer = request.form.get("answer")
        faq.display_order = int(request.form.get("display_order", 0))
        faq.is_active = request.form.get("is_active") == "on"
        
        from app import db
        db.session.commit()
        
        flash('FAQ başarıyla güncellendi!', 'success')
    except Exception as e:
        flash(f'FAQ güncellenirken hata oluştu: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_faq'))

@admin_bp.route("/faq/delete/<int:faq_id>", methods=["POST"])
@admin_required
def delete_faq(faq_id):
    try:
        faq = FAQ.query.get_or_404(faq_id)
        from app import db
        db.session.delete(faq)
        db.session.commit()
        
        flash('FAQ başarıyla silindi!', 'success')
    except Exception as e:
        flash(f'FAQ silinirken hata oluştu: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_faq'))

# Slider Yönetimi
@admin_bp.route("/slider")
@admin_required
def manage_slider():
    try:
        slider_images = Image.query.filter_by(category='slider').order_by(Image.display_order).all()
        return render_template("admin_slider.html", slider_images=slider_images)
    except Exception as e:
        flash(f'Slider yönetimi hatası: {str(e)}', 'danger')
        return render_template("admin_slider.html", slider_images=[])

@admin_bp.route("/slider/upload", methods=["POST"])
@admin_required
def upload_slider_image():
    if 'image' not in request.files:
        flash('Dosya seçilmedi!', 'danger')
        return redirect(url_for('admin.manage_slider'))
    
    file = request.files['image']
    display_order = int(request.form.get("display_order", 0))
    
    if file.filename == '':
        flash('Dosya seçilmedi!', 'danger')
        return redirect(url_for('admin.manage_slider'))
    
    if file:
        filename = secure_filename(file.filename)
        upload_folder = 'app/static/images'
        
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Veritabanına kaydet
        image = Image(
            filename=filename,
            category='slider',
            display_order=display_order
        )
        from app import db
        db.session.add(image)
        db.session.commit()
        
        flash('Slider fotoğrafı başarıyla yüklendi!', 'success')
    
    return redirect(url_for('admin.manage_slider'))

@admin_bp.route("/slider/delete/<int:image_id>", methods=["POST"])
@admin_required
def delete_slider_image(image_id):
    try:
        image = Image.query.get_or_404(image_id)
        filename = image.filename
        
        file_path = os.path.join('app', 'static', 'images', filename)
        
        # Dosyayı sil
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                flash(f'"{filename}" dosyası başarıyla silindi!', 'success')
            except OSError as e:
                flash(f'Dosya silinirken hata oluştu: {str(e)}', 'danger')
                return redirect(url_for('admin.manage_slider'))
        else:
            flash(f'"{filename}" dosyası bulunamadı, ancak veritabanından silindi.', 'warning')
        
        # Veritabanından sil
        from app import db
        db.session.delete(image)
        db.session.commit()
        
        flash(f'"{filename}" slider fotoğrafı başarıyla silindi!', 'success')
        
    except Exception as e:
        flash(f'Slider fotoğrafı silinirken hata oluştu: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_slider'))

# Gelişmiş Fotoğraf Yönetimi
@admin_bp.route("/scan-images", methods=["POST"])
@admin_required
def scan_images():
    """Mevcut fotoğrafları tarayıp veritabanına ekle"""
    try:
        import os
        from werkzeug.utils import secure_filename
        
        images_dir = "app/static/images"
        added_count = 0
        skipped_count = 0
        
        # Ana images klasöründeki slider fotoğrafları
        if os.path.exists(images_dir):
            for filename in os.listdir(images_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    # Slider fotoğrafı olarak ekle
                    existing_image = Image.query.filter_by(filename=filename, category='slider').first()
                    if not existing_image:
                        image = Image(
                            filename=filename,
                            category='slider',
                            display_order=added_count + 1,
                            is_active=True
                        )
                        db.session.add(image)
                        added_count += 1
        
        # Oda klasörlerini tara
        room_types = ['standart', 'deluxe', 'suit']
        for room_type in room_types:
            room_dir = os.path.join(images_dir, room_type)
            if os.path.exists(room_dir):
                for filename in os.listdir(room_dir):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        # Oda fotoğrafı olarak ekle
                        existing_image = Image.query.filter_by(
                            filename=filename, 
                            category='room', 
                            room_type=room_type.capitalize()
                        ).first()
                        
                        if not existing_image:
                            image = Image(
                                filename=filename,
                                category='room',
                                room_type=room_type.capitalize(),
                                display_order=added_count + 1,
                                is_active=True
                            )
                            db.session.add(image)
                            added_count += 1
                        else:
                            skipped_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'added': added_count,
            'skipped': skipped_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@admin_bp.route("/images/toggle-status/<int:image_id>", methods=["POST"])
@admin_required
def toggle_image_status(image_id):
    """Fotoğraf durumunu değiştir (aktif/pasif)"""
    try:
        image = Image.query.get_or_404(image_id)
        image.is_active = not image.is_active
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_active': image.is_active
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@admin_bp.route("/images/update-order", methods=["POST"])
@admin_required
def update_image_order():
    """Fotoğraf görüntüleme sırasını güncelle"""
    try:
        data = request.get_json()
        image_id = data.get('image_id')
        new_order = data.get('display_order', 0)
        
        image = Image.query.get_or_404(image_id)
        image.display_order = new_order
        db.session.commit()
        
        return jsonify({
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
