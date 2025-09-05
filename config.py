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
    
    # MySQL - Host Interno para desenvolvimento local
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'erp_admin'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '8de3405e496812d04fc7'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'divisions_bhs_erp_bd'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'erp'
    
    # URL de conexão MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # Engine options para MySQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': 3600,  # 1 hora
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10,
        'echo': False,  # Para debug, mude para True se quiser ver as queries SQL
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 30,
            'write_timeout': 30
        }
    }

class ProductionConfig(Config):
    """Configuração para produção"""
    
    DEBUG = False
    
    # MySQL - Host para produção no Easy Panel
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'erp_admin'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '8de3405e496812d04fc7'
    # No Easy Panel, use o host interno se disponível
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'divisions_bhs_erp_bd'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'erp'
    
    # URL de conexão MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # Engine options otimizadas para produção
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600,  # 1 hora
        'pool_pre_ping': True,
        'max_overflow': 20,
        'echo': False,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 30,
            'write_timeout': 30,
            'autocommit': True
        }
    }

class LocalConfig(Config):
    """Configuração para desenvolvimento local usando host externo"""
    
    DEBUG = True
    
    # MySQL - Host Externo para desenvolvimento local
    MYSQL_USER = 'erp_admin'
    MYSQL_PASSWORD = '8de3405e496812d04fc7'
    MYSQL_HOST = 'easypanel.pontocomdesconto.com.br'
    MYSQL_PORT = '33070'
    MYSQL_DATABASE = 'erp'
    
    # URL de conexão MySQL
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # Engine options para desenvolvimento local
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 3,
        'max_overflow': 5,
        'echo': True,  # Para ver as queries SQL em desenvolvimento
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 30,
            'write_timeout': 30
        }
    }

class InternalConfig(Config):
    """Configuração para ambiente interno (usando host interno)"""
    
    DEBUG = False
    
    # MySQL - Host Interno
    MYSQL_USER = 'erp_admin'
    MYSQL_PASSWORD = '8de3405e496812d04fc7'
    MYSQL_HOST = 'divisions_bhs_erp_bd'
    MYSQL_PORT = '3306'
    MYSQL_DATABASE = 'erp'
    
    # URL de conexão MySQL
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # Engine options para ambiente interno
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 8,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 15,
        'echo': False,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 30,
            'write_timeout': 30
        }
    }

# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,  # Agora usa host externo
    'production': ProductionConfig,
    'local': LocalConfig,              # Alternativa para desenvolvimento local
    'internal': InternalConfig,        # Para quando estiver no ambiente interno
    'default': DevelopmentConfig       # Padrão mudou para DevelopmentConfig
}