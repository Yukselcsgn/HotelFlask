from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Blueprint'leri burada kaydet
    from app.routes.main import main_bp
    from app.routes.reservation import reservation_bp
    from app.routes.admin import admin_bp
    from app.routes.sitemap import sitemap_bp
    from app.routes.robots import robots_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(reservation_bp, url_prefix="/reserve")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(sitemap_bp)
    app.register_blueprint(robots_bp)

    # Modelleri import et
    from app.models.reservation import Reservation, RoomPrice, Image

    return app
