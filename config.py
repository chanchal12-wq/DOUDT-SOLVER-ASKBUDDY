import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'askbuddy.db')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

    # SSL
    SSL_CERT = os.path.join(os.path.dirname(__file__), 'ssl', 'cert.pem')
    SSL_KEY  = os.path.join(os.path.dirname(__file__), 'ssl', 'key.pem')

    # Security headers
    SESSION_COOKIE_SECURE   = False  # set True only when running behind real HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600
