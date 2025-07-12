import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Mail ayarları - SendGrid için
class SendGridConfig(Config):
    MAIL_SERVER = "smtp.sendgrid.net"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "apikey"  # SendGrid için sabit
    MAIL_PASSWORD = os.environ.get("SENDGRID_API_KEY")
    MAIL_DEFAULT_SENDER = os.environ.get("SENDGRID_FROM_EMAIL")
    OWNER_EMAIL = os.environ.get("OWNER_EMAIL", "otel.sahibi@example.com")

class DevelopmentConfig(SendGridConfig):
    DEBUG = True

class ProductionConfig(SendGridConfig):
    DEBUG = False