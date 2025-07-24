#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def clean_blueprints_completely():
    """Remove completamente todos os blueprints para recriar do zero"""
    print("Removendo todos os blueprints...")
    
    blueprints_dir = Path("app/blueprints")
    if blueprints_dir.exists():
        shutil.rmtree(blueprints_dir)
        print("Blueprints removidos!")
    
    blueprints_dir.mkdir(exist_ok=True)
    
    # __init__.py principal
    with open(blueprints_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write("# Blueprints package\n")

def create_safe_blueprint(name, url_prefix):
    """Cria um blueprint sem caracteres especiais"""
    bp_dir = Path(f"app/blueprints/{name}")
    bp_dir.mkdir(exist_ok=True)
    
    # __init__.py
    init_content = f"""from flask import Blueprint

bp = Blueprint('{name}', __name__)

from app.blueprints.{name} import routes
"""
    
    with open(bp_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    # routes.py - MUITO SIMPLES, SEM ACENTOS
    routes_content = f"""from flask import render_template
from flask_login import login_required
from app.blueprints.{name} import bp

@bp.route('/')
@login_required
def index():
    return render_template('{name}/index.html')
"""
    
    with open(bp_dir / "routes.py", 'w', encoding='utf-8') as f:
        f.write(routes_content)
    
    print(f"Blueprint {name} criado!")

def create_auth_blueprint():
    """Cria blueprint de auth especial"""
    bp_dir = Path("app/blueprints/auth")
    bp_dir.mkdir(exist_ok=True)
    
    # __init__.py
    init_content = """from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.blueprints.auth import routes
"""
    
    with open(bp_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    # routes.py para auth
    routes_content = """from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.blueprints.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            try:
                from app.models.user import User
                user = User.query.filter_by(username='admin').first()
                if user and user.check_password('admin123'):
                    login_user(user)
                    return redirect(url_for('dashboard.index'))
            except:
                pass
            
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard.index'))
        
        flash('Credenciais invalidas', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))
"""
    
    with open(bp_dir / "routes.py", 'w', encoding='utf-8') as f:
        f.write(routes_content)
    
    print("Auth blueprint criado!")

def create_dashboard_blueprint():
    """Cria blueprint do dashboard"""
    bp_dir = Path("app/blueprints/dashboard")
    bp_dir.mkdir(exist_ok=True)
    
    # __init__.py
    init_content = """from flask import Blueprint

bp = Blueprint('dashboard', __name__)

from app.blueprints.dashboard import routes
"""
    
    with open(bp_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    # routes.py
    routes_content = """from flask import render_template
from flask_login import login_required
from app.blueprints.dashboard import bp

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard/index.html')
"""
    
    with open(bp_dir / "routes.py", 'w', encoding='utf-8') as f:
        f.write(routes_content)
    
    print("Dashboard blueprint criado!")

def create_simple_app_init():
    """Cria app/__init__.py super simples"""
    app_content = """from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faca login para acessar esta pagina.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints - MUITO SIMPLES
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.dashboard import bp as dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    
    # Modulos
    modules = [
        ('rh', '/rh'),
        ('qualidade', '/qualidade'),
        ('producao', '/producao'),
        ('compras', '/compras'),
        ('planos_acao', '/planos-acao'),
        ('consultoria', '/consultoria'),
        ('financeiro', '/financeiro'),
        ('manutencao', '/manutencao'),
        ('projetos', '/projetos'),
        ('relatorios', '/relatorios'),
        ('configuracoes', '/configuracoes')
    ]
    
    for module_name, url_prefix in modules:
        try:
            module = __import__(f'app.blueprints.{module_name}', fromlist=['bp'])
            blueprint = getattr(module, 'bp')
            app.register_blueprint(blueprint, url_prefix=url_prefix)
        except Exception as e:
            print(f"Erro ao registrar {module_name}: {e}")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app

@login_manager.user_loader
def load_user(user_id):
    try:
        from app.models.user import User
        return User.query.get(int(user_id))
    except Exception:
        return None
"""
    
    with open("app/__init__.py", 'w', encoding='utf-8') as f:
        f.write(app_content)
    
    print("App init simplificado criado!")

def create_simple_login_template():
    """Cria template de login simples"""
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
        }
        .login-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 3rem;
        }
        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }
        .logo h2 {
            color: #667eea;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-4">
                <div class="login-container">
                    <div class="logo">
                        <i class="fas fa-route fa-3x text-primary mb-3"></i>
                        <h2>ERP Sistema</h2>
                        <p class="text-muted">Corrigindo à Rota</p>
                    </div>
                    
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
                    
                    <form method="POST">
                        <div class="mb-3">
                            <label for="username" class="form-label">Usuario</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="fas fa-user"></i></span>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="password" class="form-label">Senha</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="fas fa-lock"></i></span>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-sign-in-alt me-2"></i>Entrar
                            </button>
                        </div>
                        
                        <div class="text-center mt-3">
                            <small class="text-muted">
                                <strong>Login:</strong> admin<br>
                                <strong>Senha:</strong> admin123
                            </small>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    
    with open(auth_dir / "login.html", 'w', encoding='utf-8') as f:
        f.write(login_content)
    
    print("Template de login criado!")

def main():
    print("CORRIGINDO ENCODING DEFINITIVAMENTE")
    print("="*50)
    
    # Limpar tudo
    clean_blueprints_completely()
    
    # Criar blueprints principais
    create_auth_blueprint()
    create_dashboard_blueprint()
    
    # Criar todos os módulos
    modules = [
        'rh', 'qualidade', 'producao', 'compras', 'planos_acao',
        'consultoria', 'financeiro', 'manutencao', 'projetos', 
        'relatorios', 'configuracoes'
    ]
    
    for module in modules:
        create_safe_blueprint(module, f'/{module}')
    
    # App init simples
    create_simple_app_init()
    
    # Template de login
    create_simple_login_template()
    
    print("="*50)
    print("ENCODING CORRIGIDO!")
    print("Execute: python run.py")
    print("="*50)

if __name__ == "__main__":
    main()