import os
from datetime import timedelta

class Config:
    """Configuração base"""
    
    # Chave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Configurações WTF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    
    DEBUG = True
    
    # Banco SQLite local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
    
    # Engine options para SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30
        }
    }

class ProductionConfig(Config):
    """Configuração para produção"""
    
    DEBUG = False
    
    # Banco de dados da URL de ambiente
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Se não tiver DATABASE_URL, usar SQLite como fallback
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db'
        )
    
    # Correção para URLs do Heroku/Railway que podem usar postgres://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    # Engine options mais robustas para produção
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20
    }

class RailwayConfig(ProductionConfig):
    """Configuração específica para Railway"""
    
    # Railway fornece essas variáveis
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"postgresql://{os.environ.get('RAILWAY_DB_USER', 'user')}:" \
        f"{os.environ.get('RAILWAY_DB_PASSWORD', 'pass')}@" \
        f"{os.environ.get('RAILWAY_DB_HOST', 'localhost')}:" \
        f"{os.environ.get('RAILWAY_DB_PORT', '5432')}/" \
        f"{os.environ.get('RAILWAY_DB_NAME', 'railway')}"

# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'railway': RailwayConfig,
    'default': DevelopmentConfig
}