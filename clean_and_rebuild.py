#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar e recriar o sistema do zero
"""

import os
import sys
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def clean_blueprints():
    """Remove e recria estrutura de blueprints"""
    print("Limpando estrutura de blueprints...")
    
    blueprints_dir = Path("app/blueprints")
    if blueprints_dir.exists():
        shutil.rmtree(blueprints_dir)
        print("Diretorio blueprints removido")
    
    # Recriar estrutura
    blueprints = [
        'auth', 'dashboard', 'rh', 'qualidade', 'producao', 
        'compras', 'planos_acao', 'consultoria', 'financeiro', 
        'manutencao', 'projetos', 'relatorios', 'configuracoes'
    ]
    
    # Criar diretório principal
    blueprints_dir.mkdir(exist_ok=True)
    
    # __init__.py vazio
    with open(blueprints_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write("# Blueprints package\n")
    
    for bp_name in blueprints:
        bp_dir = blueprints_dir / bp_name
        bp_dir.mkdir(exist_ok=True)
        
        # __init__.py do blueprint
        init_content = f"""from flask import Blueprint

bp = Blueprint('{bp_name}', __name__, template_folder='templates')

from app.blueprints.{bp_name} import routes
"""
        with open(bp_dir / "__init__.py", 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        # routes.py básico
        if bp_name == 'auth':
            routes_content = """from flask import render_template, redirect, url_for, flash, request
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
        elif bp_name == 'dashboard':
            routes_content = """from flask import render_template
from flask_login import login_required
from app.blueprints.dashboard import bp

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard/index.html')
"""
        else:
            routes_content = f"""from flask import render_template
from flask_login import login_required
from app.blueprints.{bp_name} import bp

@bp.route('/')
@login_required
def index():
    return render_template('{bp_name}/index.html')
"""
        
        with open(bp_dir / "routes.py", 'w', encoding='utf-8') as f:
            f.write(routes_content)
    
    print("Estrutura de blueprints recriada")

def clean_models():
    """Limpa e recria modelos básicos"""
    print("Limpando modelos...")
    
    models_dir = Path("app/models")
    if models_dir.exists():
        # Manter apenas user.py e __init__.py
        for file in models_dir.glob("*.py"):
            if file.name not in ['__init__.py', 'user.py']:
                file.unlink()
                print(f"Removido {file.name}")
    
    # Recriar __init__.py simplificado
    init_content = """from .user import User

__all__ = ['User']
"""
    with open(models_dir / "__init__.py", 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print("Modelos limpos")

def create_minimal_app():
    """Cria app/__init__.py mínimo"""
    print("Criando app minimo...")
    
    app_init = """from flask import Flask, render_template
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
    
    # Register blueprints
    try:
        from app.blueprints.auth import bp as auth_bp
        from app.blueprints.dashboard import bp as dashboard_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(dashboard_bp, url_prefix='/')
        
        print("Blueprints basicos registrados")
        
        # Outros blueprints opcionais
        other_blueprints = [
            ('rh', '/rh'), ('qualidade', '/qualidade'), ('producao', '/producao'),
            ('compras', '/compras'), ('planos_acao', '/planos-acao'), 
            ('consultoria', '/consultoria'), ('financeiro', '/financeiro'),
            ('manutencao', '/manutencao'), ('projetos', '/projetos'),
            ('relatorios', '/relatorios'), ('configuracoes', '/configuracoes')
        ]
        
        for bp_name, url_prefix in other_blueprints:
            try:
                module = __import__(f'app.blueprints.{bp_name}', fromlist=['bp'])
                blueprint = getattr(module, 'bp')
                app.register_blueprint(blueprint, url_prefix=url_prefix)
            except Exception as e:
                print(f"Blueprint {bp_name} nao carregado: {e}")
        
    except Exception as e:
        print(f"Erro ao registrar blueprints: {e}")
    
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
        f.write(app_init)
    print("App minimo criado")

def create_forms():
    """Cria formulários básicos"""
    print("Criando formularios...")
    
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
    
    print("Formularios criados")

def create_simple_templates():
    """Cria templates básicos"""
    print("Criando templates basicos...")
    
    # Dashboard simples
    dashboard_dir = Path("app/templates/dashboard")
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    
    dashboard_content = """{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="container-fluid">
    <h1 class="h3 mb-4 text-gray-800">Dashboard - Sistema ERP</h1>
    
    <div class="alert alert-success" role="alert">
        <h4 class="alert-heading">Sistema funcionando!</h4>
        <p>Bem-vindo ao ERP Corrigindo à Rota. O sistema está funcionando corretamente.</p>
        <hr>
        <p class="mb-0">Versão: 1.0.0 | Usuário: {{ current_user.username if current_user.is_authenticated else 'Anônimo' }}</p>
    </div>
    
    <div class="row">
        <div class="col-md-3">
            <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Status</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">Online</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-check-circle fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card border-left-success shadow h-100 py-2">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Usuário</div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">{{ current_user.get_display_name() if current_user.is_authenticated else 'Admin' }}</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-user fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card shadow mt-4">
        <div class="card-header">
            <h6 class="m-0 font-weight-bold text-primary">Módulos Disponíveis</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-users fa-2x text-info mb-3"></i>
                            <h5>RH</h5>
                            <a href="/rh" class="btn btn-info btn-sm">Acessar</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-tasks fa-2x text-success mb-3"></i>
                            <h5>Planos de Ação</h5>
                            <a href="/planos-acao" class="btn btn-success btn-sm">Acessar</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-chart-bar fa-2x text-warning mb-3"></i>
                            <h5>Relatórios</h5>
                            <a href="/relatorios" class="btn btn-warning btn-sm">Acessar</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    
    with open(dashboard_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(dashboard_content)
    
    # Templates básicos para outros módulos
    modules = ['rh', 'qualidade', 'producao', 'compras', 'planos_acao', 
               'consultoria', 'financeiro', 'manutencao', 'projetos', 'relatorios']
    
    for module in modules:
        module_dir = Path(f"app/templates/{module}")
        module_dir.mkdir(parents=True, exist_ok=True)
        
        module_content = f"""{{%extends "base.html" %}}

{{%block title %}}{module.replace('_', ' ').title()}{{%endblock %}}

{{%block content %}}
<div class="container-fluid">
    <h1 class="h3 mb-4 text-gray-800">Módulo {module.replace('_', ' ').title()}</h1>
    
    <div class="alert alert-info" role="alert">
        <h4 class="alert-heading">Em Desenvolvimento</h4>
        <p>Este módulo está sendo desenvolvido e estará disponível em breve.</p>
        <hr>
        <a href="/" class="btn btn-primary">Voltar ao Dashboard</a>
    </div>
</div>
{{%endblock %}}
"""
        with open(module_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(module_content)
    
    print("Templates basicos criados")

def main():
    """Função principal"""
    print("LIMPEZA E RECONSTRUCAO COMPLETA")
    print("="*50)
    
    # Limpeza
    clean_blueprints()
    clean_models()
    
    # Reconstrução
    create_minimal_app()
    create_forms()
    create_simple_templates()
    
    print("="*50)
    print("RECONSTRUCAO CONCLUIDA!")
    print("Proximos passos:")
    print("   1. python create_admin_direct.py")
    print("   2. python run.py")
    print("="*50)

if __name__ == "__main__":
    main()