#!/usr/bin/env python3
"""
Configuração específica para Easy Panel
"""
import os
from datetime import timedelta

class EasyPanelConfig:
    """Configuração específica para Easy Panel"""
    
    # Debug
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Chave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'easy-panel-secret-key-2024'
    
    # MySQL - Easy Panel usa host interno
    MYSQL_USER = 'erp_admin'
    MYSQL_PASSWORD = '8de3405e496812d04fc7'
    MYSQL_HOST = 'divisions_bhs_erp_bd'  # Host interno do Easy Panel
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'erp'
    
    # URL do banco - prioriza variável de ambiente
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
    
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = DEBUG
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
        'echo': DEBUG,
        'connect_args': {
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 30,
            'write_timeout': 30
        }
    }
    
    # Sessões
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Easy Panel pode não usar HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # WTF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações específicas"""
        
        # Log da configuração
        app.logger.info("🔧 Usando EasyPanelConfig")
        app.logger.info(f"🗄️  Database: {app.config['MYSQL_DATABASE']}")
        app.logger.info(f"🖥️  Host: {app.config['MYSQL_HOST']}:{app.config['MYSQL_PORT']}")
        app.logger.info(f"🐛 Debug: {app.config['DEBUG']}")


# Função para testar configuração
def test_config():
    """Testa a configuração"""
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config.from_object(EasyPanelConfig)
    EasyPanelConfig.init_app(app)
    
    db = SQLAlchemy(app)
    
    with app.app_context():
        try:
            # Testa conexão
            result = db.engine.execute("SELECT 1").scalar()
            print(f"✅ Configuração OK: {result}")
            return True
        except Exception as e:
            print(f"❌ Erro na configuração: {e}")
            return False

if __name__ == "__main__":
    test_config()