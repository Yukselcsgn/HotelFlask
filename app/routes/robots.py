from flask import Blueprint, make_response, render_template

robots_bp = Blueprint("robots", __name__)

@robots_bp.route("/robots.txt")
def robots():
    """Robots.txt dosyasını oluştur"""
    
    robots_content = render_template('robots.txt')
    
    response = make_response(robots_content)
    response.headers["Content-Type"] = "text/plain"
    
    return response 