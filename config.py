import os
from datetime import timedelta
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 60,
            'write_timeout': 60,
        }
    }
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    
    # Email configuration (para futuras implementações)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Pagination
    POSTS_PER_PAGE = 25
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # Usar SQLite para desenvolvimento local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    # MySQL para produção (Railway)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"mysql+pymysql://{os.environ.get('RAILWAY_DB_USER')}:" \
        f"{os.environ.get('RAILWAY_DB_PASSWORD')}@" \
        f"{os.environ.get('RAILWAY_DB_HOST')}:" \
        f"{os.environ.get('RAILWAY_DB_PORT')}/" \
        f"{os.environ.get('RAILWAY_DB_NAME')}"
    
    # Configurações de segurança para produção
    SESSION_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log para syslog em produção
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

class RailwayConfig(Config):
    """Configuração específica para Railway"""
    DEBUG = False
    
    # Construir URL do banco Railway
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.environ.get('RAILWAY_DB_USER', 'root')}:"
        f"{os.environ.get('RAILWAY_DB_PASSWORD')}@"
        f"{os.environ.get('RAILWAY_DB_HOST')}:"
        f"{os.environ.get('RAILWAY_DB_PORT', '3306')}/"
        f"{os.environ.get('RAILWAY_DB_NAME', 'railway')}"
        f"?charset=utf8mb4"
    )
    
    # Configurações otimizadas para Railway
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 60,
            'write_timeout': 60,
            'sql_mode': 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO',
        }
    }
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configurações específicas do Railway
        import logging
        logging.basicConfig(level=logging.INFO)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'railway': RailwayConfig,
    'default': DevelopmentConfig
}