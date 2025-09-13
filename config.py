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
    """Configuração para desenvolvimento - EasyPanel Externa"""
    
    DEBUG = True
    
    # MySQL - EasyPanel Host Externo
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'erp_admin'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '8de3405e496812d04fc7'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'easypanel.pontocomdesconto.com.br'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '33070'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'erp'
    
    # URL de conexão MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # Engine options para MySQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 30,
        'pool_recycle': 3600,  # 1 hora
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10,
        'echo': False,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 30,
            'write_timeout': 30
        }
    }

class ProductionConfig(Config):
    """Configuração para produção - EasyPanel Interno"""
    
    DEBUG = False
    
    # MySQL - EasyPanel Host Interno (quando rodando no próprio servidor)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'erp_admin'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '8de3405e496812d04fc7'
    # Tentar primeiro o host interno, depois externo como fallback
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
            'write_timeout': 30
        }
    }

class ExternalConfig(Config):
    """Configuração forçando conexão externa - EasyPanel"""
    
    DEBUG = False
    
    # MySQL - Forçar Host Externo EasyPanel
    MYSQL_USER = 'erp_admin'
    MYSQL_PASSWORD = '8de3405e496812d04fc7'
    MYSQL_HOST = 'easypanel.pontocomdesconto.com.br'
    MYSQL_PORT = '33070'
    MYSQL_DATABASE = 'erp'
    
    # URL de conexão MySQL
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # Engine options para conexão externa
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10,
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
    'development': DevelopmentConfig,   # Usa host externo EasyPanel
    'production': ProductionConfig,     # Usa host interno com fallback
    'external': ExternalConfig,         # Força host externo sempre
    'default': ExternalConfig           # Mudança: padrão agora é forçar externo
}