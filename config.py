import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-super-seguro-mude-em-producao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hora
    
    # Session configuration  
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    
    # Pagination
    POSTS_PER_PAGE = 25
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLite local para desenvolvimento
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class RailwayConfig(Config):
    DEBUG = False
    
    # Railway MySQL com configuracoes otimizadas
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.environ.get('RAILWAY_DB_USER', 'root')}:"
        f"{os.environ.get('RAILWAY_DB_PASSWORD')}@"
        f"{os.environ.get('RAILWAY_DB_HOST')}:"
        f"{os.environ.get('RAILWAY_DB_PORT', '3306')}/"
        f"{os.environ.get('RAILWAY_DB_NAME', 'railway')}"
        f"?charset=utf8mb4&connect_timeout=60&read_timeout=120&write_timeout=120"
    )
    
    # Configuracoes especificas para Railway
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 10,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 120, 
            'write_timeout': 120,
            'autocommit': True,
        }
    }

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'railway': RailwayConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }