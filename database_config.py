#!/usr/bin/env python3
"""
Configurações do banco de dados - EasyPanel
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-mude-em-producao')
    
    # Configurações do banco de dados EasyPanel
    DB_HOST = os.getenv('DB_HOST', 'easypanel.pontocomdesconto.com.br')
    DB_USER = os.getenv('DB_USER', 'erp_admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '8de3405e496812d04fc7')
    DB_PORT = int(os.getenv('DB_PORT', 33070))  # Porta externa do EasyPanel
    DB_NAME = os.getenv('DB_NAME', 'erp')
    
    # URL do banco
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 120,
            'write_timeout': 120
        }
    }
    
    # Configurações da empresa
    COMPANY_NAME = os.getenv('COMPANY_NAME', 'Corrigindo à Rota Industria Ltda')
    COMPANY_EMAIL = os.getenv('COMPANY_EMAIL', 'contato@corrigindoarota.com.br')

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Para produção no EasyPanel, usar host interno se disponível
    DB_HOST = os.getenv('DB_HOST', 'divisions_bhs_erp_bd')  # Host interno do EasyPanel
    DB_PORT = int(os.getenv('DB_PORT', 3306))  # Porta interna
    
    # Recriar URL com configurações de produção
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{Config.DB_NAME}"

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}