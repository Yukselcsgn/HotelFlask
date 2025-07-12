from flask import Blueprint, make_response, render_template
from datetime import datetime
from app.models.reservation import RoomPrice

sitemap_bp = Blueprint("sitemap", __name__)

@sitemap_bp.route("/sitemap.xml")
def sitemap():
    """Sitemap.xml dosyasını oluştur"""
    
    # Ana sayfalar
    pages = [
        {
            'loc': '/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '1.0'
        },
        {
            'loc': '/rooms',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.8'
        },
        {
            'loc': '/reserve',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.9'
        }
    ]
    
    # Oda sayfaları (her oda tipi için)
    try:
        room_prices = RoomPrice.query.all()
        for room in room_prices:
            pages.append({
                'loc': f'/rooms#{room.room_type.lower().replace(" ", "-")}',
                'lastmod': room.updated_at.strftime('%Y-%m-%d') if room.updated_at else datetime.now().strftime('%Y-%m-%d'),
                'changefreq': 'weekly',
                'priority': '0.7'
            })
    except:
        pass
    
    # XML oluştur
    xml_content = render_template('sitemap.xml', pages=pages, base_url='https://altunpansiyon.com')
    
    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    
    return response 