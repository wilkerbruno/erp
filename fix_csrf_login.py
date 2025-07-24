#!/usr/bin/env python3
"""
Script para corrigir problema de CSRF no login
"""

import os
from pathlib import Path

def create_forms():
    """Cria formulários com CSRF correto"""
    print("Criando formulários com CSRF...")
    
    forms_dir = Path("app/forms")
    forms_dir.mkdir(exist_ok=True)
    
    # __init__.py
    forms_init = """from .auth import LoginForm

__all__ = ['LoginForm']
"""
    with open(forms_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write(forms_init)
    
    # auth.py
    auth_form = """from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message='Campo obrigatorio'),
        Length(min=3, max=50)
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Campo obrigatorio'),
        Length(min=3)
    ])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')
"""
    with open(forms_dir / "auth.py", 'w', encoding='utf-8') as f:
        f.write(auth_form)
    
    print("✅ Formulários criados!")

def fix_auth_routes():
    """Corrige rotas de auth com CSRF"""
    print("Corrigindo rotas de auth...")
    
    auth_routes = """from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.blueprints.auth import bp
from app.forms.auth import LoginForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        try:
            from app.models.user import User
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password) and user.ativo:
                login_user(user, remember=remember_me)
                
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('dashboard.index')
                
                flash('Login realizado com sucesso!', 'success')
                return redirect(next_page)
            else:
                flash('Credenciais invalidas', 'error')
        except Exception as e:
            flash('Erro no sistema. Tente novamente.', 'error')
            print(f"Erro durante login: {e}")
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))
"""
    
    auth_dir = Path("app/blueprints/auth")
    with open(auth_dir / "routes.py", 'w', encoding='utf-8') as f:
        f.write(auth_routes)
    
    print("✅ Rotas de auth corrigidas!")

def create_login_template_with_csrf():
    """Cria template de login com CSRF token"""
    print("Criando template de login com CSRF...")
    
    auth_dir = Path("app/templates/auth")
    auth_dir.mkdir(parents=True, exist_ok=True)
    
    login_content = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - ERP Corrigindo à Rota</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            font-family: 'Nunito', sans-serif;
        }
        .login-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 3rem;
            max-width: 400px;
            width: 100%;
        }
        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }
        .logo h2 {
            color: #667eea;
            font-weight: bold;
            margin-bottom: 0;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
        }
        .btn-primary:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        }
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .input-group-text {
            background-color: #f8f9fc;
            border-color: #e3e6f0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-12 d-flex justify-content-center">
                <div class="login-container">
                    <div class="logo">
                        <i class="fas fa-route fa-3x text-primary mb-3"></i>
                        <h2>ERP Sistema</h2>
                        <p class="text-muted mb-0">Corrigindo à Rota</p>
                    </div>
                    
                    <!-- Flash Messages -->
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, message in messages %}
                                <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                                    {{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    
                    <!-- Login Form -->
                    <form method="POST" novalidate>
                        {{ form.hidden_tag() }}
                        
                        <div class="mb-3">
                            {{ form.username.label(class="form-label") }}
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="fas fa-user text-muted"></i>
                                </span>
                                {{ form.username(class="form-control", placeholder="Digite seu usuário") }}
                            </div>
                            {% for error in form.username.errors %}
                                <div class="text-danger small mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                        
                        <div class="mb-3">
                            {{ form.password.label(class="form-label") }}
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="fas fa-lock text-muted"></i>
                                </span>
                                {{ form.password(class="form-control", placeholder="Digite sua senha") }}
                            </div>
                            {% for error in form.password.errors %}
                                <div class="text-danger small mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                        
                        <div class="mb-3 form-check">
                            {{ form.remember_me(class="form-check-input") }}
                            {{ form.remember_me.label(class="form-check-label") }}
                        </div>
                        
                        <div class="d-grid mb-3">
                            {{ form.submit(class="btn btn-primary btn-lg") }}
                        </div>
                        
                        <div class="text-center">
                            <div class="card bg-light">
                                <div class="card-body py-2">
                                    <small class="text-muted">
                                        <strong>Dados de Teste:</strong><br>
                                        <strong>Usuário:</strong> admin<br>
                                        <strong>Senha:</strong> admin123
                                    </small>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        // Auto-hide alerts after 5 seconds
        setTimeout(function() {
            var alerts = document.querySelectorAll('.alert-dismissible');
            alerts.forEach(function(alert) {
                var alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
                alertInstance.close();
            });
        }, 5000);
        
        // Focus no primeiro campo
        document.addEventListener('DOMContentLoaded', function() {
            var usernameField = document.getElementById('username');
            if (usernameField) {
                usernameField.focus();
            }
        });
    </script>
</body>
</html>
"""
    
    with open(auth_dir / "login.html", 'w', encoding='utf-8') as f:
        f.write(login_content)
    
    print("✅ Template de login com CSRF criado!")

def update_config_for_csrf():
    """Atualiza configuração para CSRF"""
    print("Atualizando configuração...")
    
    config_content = '''import os
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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \\
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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \\
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'railway': RailwayConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
'''
    
    with open("config.py", 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ Configuração atualizada!")

def create_simple_run_with_csrf():
    """Cria run.py funcionando com CSRF"""
    print("Criando run.py com CSRF...")
    
    run_content = '''import os
import sys
from app import create_app, db
from flask_migrate import Migrate

def get_environment():
    """Determina o ambiente com fallback"""
    database_url = os.getenv('DATABASE_URL', '')
    
    # Se tem configuracao do Railway
    if (os.getenv('RAILWAY_DB_HOST') and 
        os.getenv('RAILWAY_DB_PASSWORD')):
        return 'railway'
    
    # Se tem DATABASE_URL com railway
    if 'railway' in database_url or 'rlwy.net' in database_url:
        return 'railway'
    
    # Default para development (SQLite)
    return 'development'

def create_admin_if_needed(app):
    """Cria admin se necessario"""
    try:
        with app.app_context():
            from app.models.user import User
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                print("Criando usuario admin...")
                admin = User(
                    username='admin',
                    email='admin@corrigindoarota.com.br',
                    perfil='admin',
                    ativo=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario admin criado!")
            else:
                print("✅ Usuario admin ja existe!")
    except Exception as e:
        print(f"Erro ao criar admin: {e}")

def main():
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente detectado: {environment}")
    
    # Criar app
    try:
        app = create_app(environment)
        migrate = Migrate(app, db)
        print("✅ Aplicacao Flask criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar aplicacao: {e}")
        # Fallback para SQLite
        try:
            app = create_app('development')
            migrate = Migrate(app, db)
            print("✅ Fallback para SQLite funcionou!")
            environment = 'development'
        except Exception as fallback_error:
            print(f"❌ Fallback tambem falhou: {fallback_error}")
            return False
    
    # Criar tabelas e admin
    try:
        with app.app_context():
            db.create_all()
            print("✅ Tabelas verificadas/criadas!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    
    create_admin_if_needed(app)
    
    print("="*50)
    print("✅ Sistema pronto para uso!")
    print(f"🌍 Ambiente: {environment}")
    print(f"📍 Acesse: http://localhost:5000")
    print("🔑 Login: admin / admin123")
    print("="*50)
    
    # Iniciar servidor
    try:
        app.run(
            debug=(environment == 'development'),
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000))
        )
    except KeyboardInterrupt:
        print("\\nSistema encerrado pelo usuario")
    except Exception as e:
        print(f"Erro ao iniciar servidor: {e}")

if __name__ == '__main__':
    if not main():
        print("Falha ao inicializar sistema!")
        sys.exit(1)
'''
    
    with open("run.py", 'w', encoding='utf-8') as f:
        f.write(run_content)
    
    print("✅ Run.py com CSRF criado!")

def main():
    print("🔧 CORRIGINDO CSRF NO LOGIN")
    print("="*50)
    
    create_forms()
    fix_auth_routes()
    create_login_template_with_csrf()
    update_config_for_csrf()
    create_simple_run_with_csrf()
    
    print("="*50)
    print("✅ CSRF CORRIGIDO!")
    print("Agora o login deve funcionar perfeitamente!")
    print("Execute: python run.py")
    print("="*50)

if __name__ == "__main__":
    main()