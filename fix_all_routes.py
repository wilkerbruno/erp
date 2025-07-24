#!/usr/bin/env python3
"""
Script para corrigir todas as rotas e garantir que funcionem
"""

import os
from pathlib import Path

def create_rh_routes():
    """Cria rotas completas para RH"""
    print("Criando rotas RH...")
    
    rh_routes = '''from flask import render_template, request, jsonify
from flask_login import login_required
from app.blueprints.rh import bp

@bp.route('/')
@login_required
def index():
    """Página principal do RH"""
    return render_template('rh/index.html')

@bp.route('/colaboradores')
@login_required
def colaboradores():
    """Lista de colaboradores"""
    return render_template('rh/colaboradores.html')

@bp.route('/colaboradores/novo')
@login_required
def novo_colaborador():
    """Formulário para novo colaborador"""
    return render_template('rh/colaboradores.html')

@bp.route('/colaboradores/<int:id>')
@login_required
def ver_colaborador(id):
    """Visualizar colaborador específico"""
    return render_template('rh/colaboradores.html')

@bp.route('/colaboradores/<int:id>/editar')
@login_required
def editar_colaborador(id):
    """Editar colaborador"""
    return render_template('rh/colaboradores.html')
'''
    
    rh_dir = Path("app/blueprints/rh")
    with open(rh_dir / "routes.py", 'w', encoding='utf-8') as f:
        f.write(rh_routes)
    
    print("✅ Rotas RH criadas!")

def create_qualidade_routes():
    """Cria rotas para Qualidade"""
    print("Criando rotas Qualidade...")
    
    qual_routes = '''from flask import render_template, request, jsonify
from flask_login import login_required
from app.blueprints.qualidade import bp

@bp.route('/')
@login_required
def index():
    """Página principal da Qualidade"""
    return render_template('qualidade/index.html')

@bp.route('/nao-conformidades')
@login_required
def nao_conformidades():
    """Lista de não conformidades"""
    return render_template('qualidade/nao_conformidades.html')

@bp.route('/auditorias')
@login_required
def auditorias():
    """Lista de auditorias"""
    return render_template('qualidade/index.html')

@bp.route('/indicadores')
@login_required
def indicadores():
    """Indicadores de qualidade"""
    return render_template('qualidade/index.html')
'''
    
    qual_dir = Path("app/blueprints/qualidade")
    with open(qual_dir / "routes.py", 'w', encoding='utf-8') as f:
        f.write(qual_routes)
    
    print("✅ Rotas Qualidade criadas!")

def create_all_module_routes():
    """Cria rotas para todos os módulos"""
    print("Criando rotas para todos os módulos...")
    
    modules = [
        'producao', 'compras', 'planos_acao', 'consultoria', 
        'financeiro', 'manutencao', 'projetos', 'relatorios', 'configuracoes'
    ]
    
    for module in modules:
        module_dir = Path(f"app/blueprints/{module}")
        
        routes_content = f'''from flask import render_template, request, jsonify
from flask_login import login_required
from app.blueprints.{module} import bp

@bp.route('/')
@login_required
def index():
    """Página principal do módulo {module}"""
    return render_template('{module}/index.html')

@bp.route('/listar')
@login_required
def listar():
    """Lista itens do módulo"""
    return render_template('{module}/index.html')

@bp.route('/novo')
@login_required
def novo():
    """Criar novo item"""
    return render_template('{module}/index.html')

@bp.route('/<int:id>')
@login_required
def ver(id):
    """Ver item específico"""
    return render_template('{module}/index.html')

@bp.route('/<int:id>/editar')
@login_required
def editar(id):
    """Editar item"""
    return render_template('{module}/index.html')
'''
        
        with open(module_dir / "routes.py", 'w', encoding='utf-8') as f:
            f.write(routes_content)
    
    print(f"✅ Rotas criadas para {len(modules)} módulos!")

def update_app_init():
    """Atualiza app/__init__.py para registrar todas as rotas corretamente"""
    print("Atualizando app/__init__.py...")
    
    app_init_content = '''from flask import Flask, render_template
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
    print("Registrando blueprints...")
    
    try:
        # Blueprints principais
        from app.blueprints.auth import bp as auth_bp
        from app.blueprints.dashboard import bp as dashboard_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(dashboard_bp, url_prefix='/')
        print("✅ Auth e Dashboard registrados")
        
        # Blueprints dos módulos
        modules_config = [
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
        
        for module_name, url_prefix in modules_config:
            try:
                module = __import__(f'app.blueprints.{module_name}', fromlist=['bp'])
                blueprint = getattr(module, 'bp')
                app.register_blueprint(blueprint, url_prefix=url_prefix)
                print(f"✅ {module_name} registrado em {url_prefix}")
            except Exception as e:
                print(f"⚠️  Erro ao registrar {module_name}: {e}")
        
    except Exception as e:
        print(f"❌ Erro ao registrar blueprints: {e}")
    
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
'''
    
    with open("app/__init__.py", 'w', encoding='utf-8') as f:
        f.write(app_init_content)
    
    print("✅ app/__init__.py atualizado!")

def create_error_templates():
    """Cria templates de erro"""
    print("Criando templates de erro...")
    
    errors_dir = Path("app/templates/errors")
    errors_dir.mkdir(parents=True, exist_ok=True)
    
    # 404.html
    error_404 = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página não encontrada - ERP</title>
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
        .error-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 3rem;
            text-align: center;
        }
        .error-code {
            font-size: 8rem;
            font-weight: 900;
            color: #667eea;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="error-container">
                    <div class="error-code">404</div>
                    <div class="error-message">
                        <h2><i class="fas fa-search me-2"></i>Página Não Encontrada</h2>
                        <p class="text-muted">A página que você está procurando não existe ou foi movida.</p>
                    </div>
                    <div class="mt-4">
                        <a href="/" class="btn btn-primary me-3">
                            <i class="fas fa-home me-2"></i>Voltar ao Dashboard
                        </a>
                        <a href="javascript:history.back()" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Voltar
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    with open(errors_dir / "404.html", 'w', encoding='utf-8') as f:
        f.write(error_404)
    
    # 500.html  
    error_500 = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Erro interno - ERP</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            font-family: 'Nunito', sans-serif;
        }
        .error-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            padding: 3rem;
            text-align: center;
        }
        .error-code {
            font-size: 8rem;
            font-weight: 900;
            color: #f5576c;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="error-container">
                    <div class="error-code">500</div>
                    <div class="error-message">
                        <h2><i class="fas fa-exclamation-triangle me-2"></i>Erro Interno</h2>
                        <p class="text-muted">Ops! Algo deu errado. Nossa equipe foi notificada.</p>
                    </div>
                    <div class="mt-4">
                        <a href="/" class="btn btn-primary me-3">
                            <i class="fas fa-home me-2"></i>Voltar ao Dashboard
                        </a>
                        <a href="javascript:location.reload()" class="btn btn-outline-secondary">
                            <i class="fas fa-redo me-2"></i>Tentar Novamente
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    with open(errors_dir / "500.html", 'w', encoding='utf-8') as f:
        f.write(error_500)
    
    print("✅ Templates de erro criados!")

def create_debug_routes():
    """Cria script para debugar rotas"""
    print("Criando debug de rotas...")
    
    debug_script = '''#!/usr/bin/env python3
"""
Script para debugar e testar todas as rotas
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_routes():
    """Testa se todas as rotas estão funcionando"""
    
    try:
        from app import create_app
        
        environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
        app = create_app(environment)
        
        with app.app_context():
            print("🔍 TESTANDO TODAS AS ROTAS")
            print("="*50)
            
            # Listar todas as rotas registradas
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'url': str(rule)
                })
            
            # Organizar por blueprint
            blueprints = {}
            for route in routes:
                blueprint = route['endpoint'].split('.')[0] if '.' in route['endpoint'] else 'main'
                if blueprint not in blueprints:
                    blueprints[blueprint] = []
                blueprints[blueprint].append(route)
            
            # Mostrar rotas por blueprint
            for blueprint, blueprint_routes in blueprints.items():
                print(f"\\n📁 {blueprint.upper()}")
                print("-" * 30)
                
                for route in blueprint_routes:
                    methods = [m for m in route['methods'] if m not in ['HEAD', 'OPTIONS']]
                    print(f"  {route['url']} -> {route['endpoint']} {methods}")
            
            print("\\n" + "="*50)
            print(f"✅ Total de rotas: {len(routes)}")
            print(f"✅ Total de blueprints: {len(blueprints)}")
            
            # Testar principais rotas
            test_urls = [
                '/',
                '/rh',
                '/rh/colaboradores', 
                '/qualidade',
                '/qualidade/nao-conformidades',
                '/producao',
                '/compras',
                '/planos-acao',
                '/consultoria',
                '/financeiro',
                '/manutencao',
                '/projetos',
                '/relatorios',
                '/configuracoes'
            ]
            
            print("\\n🧪 TESTANDO URLS PRINCIPAIS")
            print("-" * 30)
            
            with app.test_client() as client:
                for url in test_urls:
                    try:
                        response = client.get(url, follow_redirects=True)
                        status = "✅" if response.status_code in [200, 302] else "❌"
                        print(f"  {status} {url} -> {response.status_code}")
                    except Exception as e:
                        print(f"  ❌ {url} -> ERRO: {e}")
            
            print("\\n" + "="*50)
            print("🎉 TESTE DE ROTAS CONCLUÍDO!")
            
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_routes()
'''
    
    with open("debug_routes.py", 'w', encoding='utf-8') as f:
        f.write(debug_script)
    
    print("✅ Debug de rotas criado!")

def main():
    """Função principal"""
    print("🔧 CORRIGINDO TODAS AS ROTAS")
    print("="*50)
    
    create_rh_routes()
    create_qualidade_routes()
    create_all_module_routes()
    update_app_init()
    create_error_templates()
    create_debug_routes()
    
    print("="*50)
    print("✅ TODAS AS ROTAS CORRIGIDAS!")
    print("📋 Próximos passos:")
    print("1. python debug_routes.py  # Para ver todas as rotas")
    print("2. python run.py           # Para executar o sistema")
    print("="*50)

if __name__ == "__main__":
    main()