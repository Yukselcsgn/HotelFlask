from flask_mail import Message
from app import mail
from flask import current_app, render_template_string
from datetime import datetime

def send_reservation_email(to_email, reservation_data):
    """Müşteriye rezervasyon onay e-postası gönder"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #111; color: #FFD700; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .reservation-details {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #FFD700; }}
            .detail-row {{ display: flex; justify-content: space-between; margin: 10px 0; }}
            .label {{ font-weight: bold; color: #111; }}
            .value {{ color: #666; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            .success-icon {{ color: #28a745; font-size: 24px; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏨 Altun Pansiyon</h1>
                <h2>Rezervasyon Onayı</h2>
            </div>
            <div class="content">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div class="success-icon">✅</div>
                    <h3>Rezervasyonunuz Başarıyla Alındı!</h3>
                </div>
                
                <p>Merhaba <strong>{reservation_data['name']}</strong>,</p>
                
                <p>Rezervasyonunuz başarıyla alınmıştır. Aşağıda rezervasyon detaylarınızı bulabilirsiniz:</p>
                
                <div class="reservation-details">
                    <div class="detail-row">
                        <span class="label">Ad Soyad:</span>
                        <span class="value">{reservation_data['name']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Telefon:</span>
                        <span class="value">{reservation_data.get('phone', 'Belirtilmemiş')}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Oda Tipi:</span>
                        <span class="value">{reservation_data['room_type']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Giriş Tarihi:</span>
                        <span class="value">{reservation_data['check_in']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Çıkış Tarihi:</span>
                        <span class="value">{reservation_data['check_out']}</span>
                    </div>
                </div>
                
                <p><strong>Önemli Bilgiler:</strong></p>
                <ul>
                    <li>Check-in saati: 14:00</li>
                    <li>Check-out saati: 11:00</li>
                    <li>Rezervasyon değişiklikleri için lütfen bizimle iletişime geçin</li>
                </ul>
                
                <p>Bizi tercih ettiğiniz için teşekkür ederiz! 🎉</p>
                
                <div class="footer">
                    <p>🏨 <strong>Altun Pansiyon</strong></p>
                    <p>📧 info@altunpansiyon.com | 📞 +90 555 555 55 55</p>
                    <p>📍 Adres: Şehir Merkezi, Altun Pansiyon, Türkiye</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    msg = Message(
        subject="✅ Rezervasyon Onayı - Altun Pansiyon",
        recipients=[to_email],
        html=html_content
    )

    with current_app.app_context():
        mail.send(msg)

def notify_owner_about_reservation(reservation_data, owner_email):
    """Otel sahibine yeni rezervasyon bildirimi gönder"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #FFD700; color: #111; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .reservation-details {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #FFD700; }}
            .detail-row {{ display: flex; justify-content: space-between; margin: 10px 0; }}
            .label {{ font-weight: bold; color: #FFD700; }}
            .value {{ color: #666; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            .notification-icon {{ color: #FFD700; font-size: 24px; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏨 Altun Pansiyon</h1>
                <h2>Yeni Rezervasyon Bildirimi</h2>
            </div>
            <div class="content">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div class="notification-icon">🔔</div>
                    <h3>Yeni Bir Rezervasyon Alındı!</h3>
                </div>
                
                <p>Yeni bir rezervasyon talebi alınmıştır. Detaylar aşağıdadır:</p>
                
                <div class="reservation-details">
                    <div class="detail-row">
                        <span class="label">Müşteri Adı:</span>
                        <span class="value">{reservation_data['name']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">E-posta:</span>
                        <span class="value">{reservation_data['email']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Telefon:</span>
                        <span class="value">{reservation_data.get('phone', 'Belirtilmemiş')}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Oda Tipi:</span>
                        <span class="value">{reservation_data['room_type']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Giriş Tarihi:</span>
                        <span class="value">{reservation_data['check_in']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Çıkış Tarihi:</span>
                        <span class="value">{reservation_data['check_out']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Rezervasyon Tarihi:</span>
                        <span class="value">{datetime.now().strftime('%d.%m.%Y %H:%M')}</span>
                    </div>
                </div>
                
                <p><strong>Hızlı İşlemler:</strong></p>
                <ul>
                    <li>✅ Rezervasyonu onayla</li>
                    <li>📞 Müşteri ile iletişime geç</li>
                    <li>📋 Oda hazırlığını planla</li>
                </ul>
                
                <div class="footer">
                    <p>🏨 <strong>Altun Pansiyon Yönetim Paneli</strong></p>
                    <p>📧 admin@altunpansiyon.com</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    msg = Message(
        subject="🔔 Yeni Rezervasyon - Altun Pansiyon",
        recipients=[owner_email],
        html=html_content
    )
    
    with current_app.app_context():
        mail.send(msg)