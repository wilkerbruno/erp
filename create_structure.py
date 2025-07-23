import os

def create_blueprint_structure():
    """Cria toda a estrutura de blueprints do projeto"""
    
    # Estrutura de blueprints
    blueprints = {
        'auth': ['login', 'logout'],
        'dashboard': ['index'],
        'rh': ['colaboradores'],
        'qualidade': ['nao_conformidades', 'auditorias'],
        'producao': ['ordens_producao', 'produtos'],
        'compras': ['index', 'fornecedores', 'nova_ordem_compra'],
        'planos_acao': ['index'],
        'consultoria': ['index', 'novo_projeto', 'produtos_consultoria'],
        'financeiro': ['dre'],
        'manutencao': ['index'],
        'projetos': ['index', 'novo_projeto'],
        'relatorios': ['index'],
        'configuracoes': ['index']
    }
    
    base_dir = 'app/blueprints'
    
    # Criar diretório base se não existir
    os.makedirs(base_dir, exist_ok=True)
    
    # Criar __init__.py do blueprints (vazio)
    with open(f'{base_dir}/__init__.py', 'w', encoding='utf-8') as f:
        f.write('# Blueprints package\n')
    
    # Criar cada blueprint
    for blueprint_name, routes in blueprints.items():
        blueprint_dir = f'{base_dir}/{blueprint_name}'
        os.makedirs(blueprint_dir, exist_ok=True)
        
        # Criar __init__.py do blueprint
        init_content = f"""from flask import Blueprint

bp = Blueprint('{blueprint_name}', __name__, template_folder='templates')

from app.blueprints.{blueprint_name} import routes
"""
        
        with open(f'{blueprint_dir}/__init__.py', 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        # Criar routes.py do blueprint
        routes_content = create_routes_content(blueprint_name, routes)
        
        with open(f'{blueprint_dir}/routes.py', 'w', encoding='utf-8') as f:
            f.write(routes_content)
    
    print("Estrutura de blueprints criada com sucesso!")

def create_routes_content(blueprint_name, routes):
    """Cria o conteúdo do arquivo routes.py para cada blueprint"""
    
    if blueprint_name == 'auth':
        return """from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.models.user import User
from app.blueprints.auth import bp
from datetime import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = bool(request.form.get('remember_me'))
        
        if not username or not password:
            flash('Por favor, preencha todos os campos.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Usuário ou senha inválidos', 'error')
            return render_template('auth/login.html')
        
        if not user.ativo:
            flash('Conta desativada. Entre em contato com o administrador.', 'error')
            return render_template('auth/login.html')
        
        login_user(user, remember=remember_me)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard.index')
        
        flash(f'Bem-vindo, {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('auth.login'))
"""
    
    elif blueprint_name == 'dashboard':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.dashboard import bp

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard/index.html')
"""
    
    elif blueprint_name == 'rh':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.rh import bp

@bp.route('/colaboradores')
@login_required
def colaboradores():
    return render_template('rh/colaboradores.html')
"""
    
    elif blueprint_name == 'qualidade':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.qualidade import bp

@bp.route('/nao-conformidades')
@login_required
def nao_conformidades():
    return render_template('qualidade/nao_conformidades.html')

@bp.route('/auditorias')
@login_required
def auditorias():
    return render_template('qualidade/auditorias.html')
"""
    
    elif blueprint_name == 'producao':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.producao import bp

@bp.route('/ordens-producao')
@login_required
def ordens_producao():
    return render_template('producao/ordens_producao.html')

@bp.route('/produtos')
@login_required
def produtos():
    return render_template('producao/produtos.html')
"""
    
    elif blueprint_name == 'compras':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.compras import bp

@bp.route('/')
@login_required
def index():
    return render_template('compras/index.html')

@bp.route('/fornecedores')
@login_required
def fornecedores():
    return render_template('compras/fornecedores.html')

@bp.route('/nova-ordem-compra')
@login_required
def nova_ordem_compra():
    return render_template('compras/nova_ordem_compra.html')
"""
    
    elif blueprint_name == 'planos_acao':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.planos_acao import bp

@bp.route('/')
@login_required
def index():
    return render_template('planos_acao/index.html')
"""
    
    elif blueprint_name == 'consultoria':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.consultoria import bp

@bp.route('/')
@login_required
def index():
    return render_template('consultoria/index.html')

@bp.route('/novo-projeto')
@login_required
def novo_projeto():
    return render_template('consultoria/novo_projeto.html')

@bp.route('/produtos-consultoria')
@login_required
def produtos_consultoria():
    return render_template('consultoria/produtos.html')
"""
    
    elif blueprint_name == 'financeiro':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.financeiro import bp

@bp.route('/dre')
@login_required
def dre():
    return render_template('financeiro/dre.html')
"""
    
    elif blueprint_name == 'manutencao':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.manutencao import bp

@bp.route('/')
@login_required
def index():
    return render_template('manutencao/index.html')
"""
    
    elif blueprint_name == 'projetos':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.projetos import bp

@bp.route('/')
@login_required
def index():
    return render_template('projetos/index.html')

@bp.route('/novo-projeto')
@login_required
def novo_projeto():
    return render_template('projetos/novo_projeto.html')
"""
    
    elif blueprint_name == 'relatorios':
        return """from flask import render_template
from flask_login import login_required
from app.blueprints.relatorios import bp

@bp.route('/')
@login_required
def index():
    return render_template('relatorios/index.html')
"""
    
    elif blueprint_name == 'configuracoes':
        return """from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.blueprints.configuracoes import bp

@bp.route('/')
@login_required
def index():
    if not current_user.has_permission('admin'):
        flash('Acesso negado para este módulo.', 'error')
        return redirect(url_for('dashboard.index'))
    return render_template('configuracoes/index.html')
"""
    
    else:
        return f"""from flask import render_template
from flask_login import login_required
from app.blueprints.{blueprint_name} import bp

@bp.route('/')
@login_required
def index():
    return render_template('{blueprint_name}/index.html')
"""

def create_static_structure():
    """Cria a estrutura de arquivos estáticos"""
    
    # Criar diretórios
    static_dirs = ['app/static/css', 'app/static/js', 'app/static/img']
    for directory in static_dirs:
        os.makedirs(directory, exist_ok=True)
    
    # Criar arquivo CSS básico
    css_content = """/* Custom CSS para o ERP Corrigindo à Rota */
body {
    font-family: 'Nunito', sans-serif;
}

.badge-notification {
    position: absolute;
    top: -5px;
    right: -5px;
    transform: scale(0.8);
}

.notification-dropdown {
    min-width: 300px;
    max-height: 400px;
    overflow-y: auto;
}

.card:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

.form-control:focus {
    border-color: #4e73df;
    box-shadow: 0 0 0 0.2rem rgba(78, 115, 223, 0.25);
}

@media (max-width: 768px) {
    .table-responsive {
        font-size: 0.875rem;
    }
}
"""
    
    with open('app/static/css/custom.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # Criar arquivo JS básico
    js_content = """// Custom JavaScript para o ERP
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
            alertInstance.close();
        });
    }, 5000);
});

function showNotification(message, type = 'info', duration = 5000) {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Implementação será expandida posteriormente
}
"""
    
    with open('app/static/js/custom.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print("Estrutura de arquivos estáticos criada!")

if __name__ == '__main__':
    create_blueprint_structure()
    create_static_structure()
    print("\n✅ Estrutura completa criada com sucesso!")
    print("Execute: python run.py")