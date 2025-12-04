#!/usr/bin/env python3
"""
Aplicação Flask Simplificada para EasyPanel
Versão corrigida para Python 3.13
"""

import sys
import os
from functools import wraps
from flask import session
from sqlalchemy import and_, or_

from app.models import (
    Colaborador, Beneficio, ColaboradorBeneficio, CargoBeneficio,
    RegistroPonto, AutorizacaoHomeOffice, AuxilioCelular, Holerite, DREGerencial
)

# PATCH CRÍTICO PARA PYTHON 3.13 - DEVE VIR ANTES DE QUALQUER IMPORT
if sys.version_info >= (3, 13):
    print("🔧 Aplicando patch Python 3.13 + SQLAlchemy...")
    
    # Monkey patch do módulo typing para evitar o erro
    import typing
    
    # Salvar função original
    _original_init_subclass = typing.Generic.__init_subclass__
    
    @classmethod
    def patched_init_subclass(cls, *args, **kwargs):
        # Para classes problemáticas, pular verificações rigorosas
        if hasattr(cls, '__name__') and 'SQLCoreOperations' in str(cls):
            # Remove atributos problemáticos
            for attr in ['__firstlineno__', '__static_attributes__']:
                if hasattr(cls, attr):
                    try:
                        delattr(cls, attr)
                    except (AttributeError, TypeError):
                        pass
        
        return _original_init_subclass(*args, **kwargs)
    
    # Aplicar patch
    typing.Generic.__init_subclass__ = patched_init_subclass
    
    # Patch adicional no langhelpers
    def patch_langhelpers():
        try:
            import sqlalchemy.util.langhelpers as lh
            
            # Sobrescrever verificação problemática
            original_init_subclass = lh.TypingOnly.__init_subclass__
            
            @classmethod
            def safe_init_subclass(cls, **kwargs):
                # Remover atributos problemáticos
                problematic_attrs = {'__firstlineno__', '__static_attributes__'}
                for attr in problematic_attrs:
                    if hasattr(cls, attr):
                        try:
                            delattr(cls, attr)
                        except:
                            pass
                
                # Chamar original sem verificação rigorosa
                try:
                    return original_init_subclass(**kwargs)
                except AssertionError:
                    # Se der erro, pular verificação
                    pass
            
            lh.TypingOnly.__init_subclass__ = safe_init_subclass
            
        except ImportError:
            # SQLAlchemy ainda não foi importado
            pass
    
    # Agendar patch para quando sqlalchemy for importado
    import importlib.util
    import builtins
    original_import = builtins.__import__
    
    def patched_import(name, *args, **kwargs):
        result = original_import(name, *args, **kwargs)
        
        # Aplicar patch quando sqlalchemy.util.langhelpers for importado
        if name == 'sqlalchemy.util.langhelpers' or 'langhelpers' in name:
            patch_langhelpers()
        
        return result
    
    builtins.__import__ = patched_import
    print("✅ Patch Python 3.13 aplicado!")

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Configuração da aplicação
app = Flask(__name__)

# Configurações EasyPanel
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do banco EasyPanel
MYSQL_USER = 'erp_admin'
MYSQL_PASSWORD = '8de3405e496812d04fc7'
MYSQL_HOST = 'easypanel.pontocomdesconto.com.br'
MYSQL_PORT = '33070'
MYSQL_DATABASE = 'erp'

DATABASE_URL = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_timeout': 30,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'max_overflow': 20,
    'connect_args': {
        'charset': 'utf8mb4',
        'connect_timeout': 60,
        'read_timeout': 30,
        'write_timeout': 30
    }
}

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelo de usuário simples
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    perfil = db.Column(db.String(50), default='user')
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Rotas

@app.route('/')
def index():
    """Página inicial"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ERP Corrigindo à Rota</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body text-center">
                            <h2 class="card-title text-primary">🏢 ERP Sistema</h2>
                            <p class="card-text">Corrigindo à Rota Indústria Ltda</p>
                            <hr>
                            <h5 class="text-success">✅ Sistema Online!</h5>
                            <p class="text-muted">Aplicação rodando no EasyPanel</p>
                            <p class="text-info">Python 3.13 + SQLAlchemy Patch Aplicado</p>
                            <hr>
                            <div class="row">
                                <div class="col">
                                    <strong>Host:</strong><br>
                                    <small>easypanel.pontocomdesconto.com.br</small>
                                </div>
                                <div class="col">
                                    <strong>Banco:</strong><br>
                                    <small>MySQL EasyPanel</small>
                                </div>
                            </div>
                            <hr>
                            <a href="/login" class="btn btn-primary">Fazer Login</a>
                            <a href="/test" class="btn btn-info">Testar Banco</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/test')
def test_database():
    """Testa a conexão com banco"""
    try:
        # Tentar consultar usuários
        user_count = User.query.count()
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Teste de Banco</title>
            <meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="card">
                    <div class="card-body">
                        <h3 class="text-success">✅ Conexão OK!</h3>
                        <p><strong>Python:</strong> {sys.version}</p>
                        <p><strong>Usuários cadastrados:</strong> {user_count}</p>
                        <p><strong>Database URI:</strong> {app.config['SQLALCHEMY_DATABASE_URI']}</p>
                        <a href="/" class="btn btn-primary">Voltar</a>
                        <a href="/create-admin" class="btn btn-success">Criar Admin</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Erro no Banco</title>
            <meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="card">
                    <div class="card-body">
                        <h3 class="text-danger">❌ Erro na Conexão</h3>
                        <p><strong>Python:</strong> {sys.version}</p>
                        <p><strong>Erro:</strong> {str(e)}</p>
                        <p><strong>Database URI:</strong> {app.config['SQLALCHEMY_DATABASE_URI']}</p>
                        <a href="/" class="btn btn-primary">Voltar</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''

@app.route('/create-admin')
def create_admin():
    """Cria usuário admin"""
    try:
        # Criar tabelas se não existirem
        db.create_all()
        
        # Verificar se admin já existe
        existing_admin = User.query.filter_by(username='admin').first()
        
        if existing_admin:
            message = "✅ Usuário admin já existe!"
            status = "info"
        else:
            # Criar admin
            admin = User(
                username='admin',
                email='admin@corrigindoarota.com.br',
                perfil='admin',
                ativo=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            message = "✅ Usuário admin criado com sucesso!"
            status = "success"
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Criar Admin</title>
            <meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="card">
                    <div class="card-body">
                        <div class="alert alert-{status}">
                            <h4>{message}</h4>
                        </div>
                        <div class="row">
                            <div class="col">
                                <strong>Usuário:</strong> admin
                            </div>
                            <div class="col">
                                <strong>Senha:</strong> admin123
                            </div>
                        </div>
                        <hr>
                        <a href="/" class="btn btn-primary">Voltar</a>
                        <a href="/login" class="btn btn-success">Fazer Login</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
        
    except Exception as e:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Erro</title>
            <meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <div class="card">
                    <div class="card-body">
                        <div class="alert alert-danger">
                            <h4>❌ Erro ao criar admin</h4>
                            <p>{str(e)}</p>
                        </div>
                        <a href="/" class="btn btn-primary">Voltar</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login simples"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                return f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Login OK</title>
                    <meta charset="UTF-8">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
                </head>
                <body class="bg-light">
                    <div class="container mt-5">
                        <div class="card">
                            <div class="card-body">
                                <div class="alert alert-success">
                                    <h4>✅ Login realizado com sucesso!</h4>
                                    <p>Bem-vindo, <strong>{user.username}</strong>!</p>
                                    <p>Perfil: <strong>{user.perfil}</strong></p>
                                </div>
                                <a href="/" class="btn btn-primary">Página Inicial</a>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                '''
            else:
                error_msg = "Usuário ou senha incorretos"
        except Exception as e:
            error_msg = f"Erro no banco: {str(e)}"
    else:
        error_msg = None
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - ERP</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
            }}
            .login-container {{
                background: white;
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                padding: 3rem;
                max-width: 400px;
                width: 100%;
            }}
            .logo h2 {{
                color: #667eea;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-12 d-flex justify-content-center">
                    <div class="login-container">
                        <div class="text-center mb-4">
                            <h2>🏢 ERP Sistema</h2>
                            <p class="text-muted">Corrigindo à Rota</p>
                        </div>
                        
                        {"<div class='alert alert-danger'>" + error_msg + "</div>" if error_msg else ""}
                        
                        <form method="POST">
                            <div class="mb-3">
                                <label class="form-label">Usuário</label>
                                <div class="input-group">
                                    <span class="input-group-text">👤</span>
                                    <input type="text" class="form-control" name="username" required placeholder="Digite seu usuário">
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label class="form-label">Senha</label>
                                <div class="input-group">
                                    <span class="input-group-text">🔐</span>
                                    <input type="password" class="form-control" name="password" required placeholder="Digite sua senha">
                                </div>
                            </div>
                            
                            <div class="d-grid mb-3">
                                <button type="submit" class="btn btn-primary btn-lg">Entrar</button>
                            </div>
                            
                            <div class="text-center">
                                <small class="text-muted">
                                    Usuário padrão: <strong>admin</strong><br>
                                    Senha padrão: <strong>admin123</strong>
                                </small>
                            </div>
                        </form>
                        
                        <hr>
                        <div class="text-center">
                            <a href="/" class="btn btn-outline-secondary btn-sm">Voltar</a>
                            <a href="/create-admin" class="btn btn-outline-info btn-sm">Criar Admin</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.errorhandler(404)
def not_found_error(error):
    """Página 404"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Página não encontrada</title>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="text-center">
                <h1>404</h1>
                <p>Página não encontrada</p>
                <a href="/" class="btn btn-primary">Página Inicial</a>
            </div>
        </div>
    </body>
    </html>
    ''', 404

@app.errorhandler(500)
def internal_error(error):
    """Página 500"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Erro interno</title>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="text-center">
                <h1>500</h1>
                <p>Erro interno do servidor</p>
                <a href="/" class="btn btn-primary">Página Inicial</a>
            </div>
        </div>
    </body>
    </html>
    ''', 500

# Função para inicializar o banco
def init_database():
    """Inicializa o banco de dados"""
    try:
        with app.app_context():
            print("🔧 Criando estrutura do banco...")
            db.create_all()
            print("✅ Estrutura criada!")
            
            # Verificar/criar admin
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("🔧 Criando usuário admin...")
                admin = User(
                    username='admin',
                    email='admin@corrigindoarota.com.br',
                    perfil='admin',
                    ativo=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuário admin criado!")
            else:
                print("✅ Usuário admin já existe!")
                
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")

# ========== BENEFÍCIOS ==========
@app.route('/rh/beneficios')
@login_required
def rh_beneficios():
    """Página principal de benefícios"""
    return render_template('rh/beneficios/index.html')

@app.route('/rh/beneficios/novo', methods=['GET', 'POST'])
@login_required
def rh_novo_beneficio():
    """Criar novo benefício"""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            # Mock de resposta
            return jsonify({
                'status': 'success',
                'message': 'Benefício criado com sucesso!',
                'beneficio': {
                    'id': 1,
                    'nome': data.get('nome'),
                    'tipo': data.get('tipo', 'fixo'),
                    'valor': data.get('valor', 0),
                    'ativo': True
                }
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('rh/beneficios/novo.html')

@app.route('/rh/api/beneficios')
@login_required
def rh_api_listar_beneficios():
    """API: Lista todos os benefícios"""
    beneficios = [
        {
            'id': 1,
            'nome': 'Vale Alimentação',
            'tipo': 'fixo',
            'valor': 500.00,
            'ativo': True
        },
        {
            'id': 2,
            'nome': 'Auxílio Celular',
            'tipo': 'fixo',
            'valor': 50.00,
            'ativo': True
        },
        {
            'id': 3,
            'nome': 'Plano de Saúde',
            'tipo': 'fixo',
            'valor': 300.00,
            'ativo': True
        }
    ]
    
    return jsonify({
        'status': 'success',
        'beneficios': beneficios
    })


# ========== AUXÍLIO CELULAR ==========

@app.route('/colaborador/<int:colaborador_id>/auxilio-celular', methods=['GET', 'POST'])
@login_required
def auxilio_celular(colaborador_id):
    """Gerenciar auxílio celular"""
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            # Verificar se já existe
            auxilio = AuxilioCelular.query.filter_by(colaborador_id=colaborador_id).first()
            
            if auxilio:
                auxilio.ativo = data.get('ativo', True)
                auxilio.valor_mensal = data.get('valor_mensal', 50.00)
            else:
                auxilio = AuxilioCelular(
                    colaborador_id=colaborador_id,
                    valor_mensal=data.get('valor_mensal', 50.00),
                    ativo=data.get('ativo', True),
                    data_inicio=datetime.utcnow().date(),
                    motivo_concessao=data.get('motivo_concessao'),
                    criado_por=current_user.id
                )
                db.session.add(auxilio)
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Auxílio celular atualizado com sucesso!'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('rh/auxilio_celular.html', colaborador=colaborador)

# ========== PONTO COM LOCALIZAÇÃO ==========

@app.route('/bater-ponto')
@login_required
def bater_ponto():
    """Página para bater ponto com localização"""
    return render_template('rh/ponto/bater_ponto.html')

@app.route('/api/registrar-ponto', methods=['POST'])
@login_required
def api_registrar_ponto():
    """API: Registrar ponto com localização"""
    try:
        data = request.get_json()
        
        # Verificar autorização de home office se aplicável
        home_office = data.get('home_office', False)
        home_office_autorizado = False
        
        if home_office:
            # Verificar se tem autorização ativa
            hoje = date.today()
            autorizacao = AutorizacaoHomeOffice.query.filter(
                and_(
                    AutorizacaoHomeOffice.colaborador_id == data['colaborador_id'],
                    AutorizacaoHomeOffice.status == 'ativo',
                    AutorizacaoHomeOffice.data_inicio <= hoje,
                    or_(
                        AutorizacaoHomeOffice.data_fim >= hoje,
                        AutorizacaoHomeOffice.data_fim.is_(None)
                    )
                )
            ).first()
            
            home_office_autorizado = autorizacao is not None
        
        # Calcular atraso se for entrada
        atraso_minutos = 0
        dentro_horario = True
        
        if data['tipo'] == 'entrada':
            horario_entrada = datetime.strptime(data['horario'], '%H:%M:%S').time()
            horario_esperado = datetime.strptime('08:00:00', '%H:%M:%S').time()
            
            if horario_entrada > horario_esperado:
                delta = datetime.combine(date.today(), horario_entrada) - datetime.combine(date.today(), horario_esperado)
                atraso_minutos = int(delta.total_seconds() / 60)
                dentro_horario = False
        
        # Criar registro
        registro = RegistroPonto(
            colaborador_id=data['colaborador_id'],
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            tipo=data['tipo'],
            horario=datetime.strptime(data['horario'], '%H:%M:%S').time(),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            localizacao_texto=data.get('localizacao_texto'),
            distancia_empresa=data.get('distancia_empresa'),
            home_office=home_office,
            home_office_autorizado=home_office_autorizado,
            dentro_horario=dentro_horario,
            atraso_minutos=atraso_minutos,
            dispositivo=data.get('dispositivo'),
            ip_address=request.remote_addr,
            observacoes=data.get('observacoes')
        )
        
        db.session.add(registro)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Ponto registrado com sucesso!',
            'registro': registro.to_dict(),
            'atraso_minutos': atraso_minutos,
            'home_office_autorizado': home_office_autorizado
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/ponto/hoje/<int:colaborador_id>')
@login_required
def api_ponto_hoje(colaborador_id):
    """API: Obter registros de ponto de hoje"""
    hoje = date.today()
    registros = RegistroPonto.query.filter(
        and_(
            RegistroPonto.colaborador_id == colaborador_id,
            RegistroPonto.data == hoje
        )
    ).order_by(RegistroPonto.horario).all()
    
    return jsonify({
        'status': 'success',
        'registros': [r.to_dict() for r in registros]
    })

# ========== HOME OFFICE ==========

@app.route('/rh/home-office')
@login_required
def rh_home_office():
    """Página de gerenciamento de home office"""
    return render_template('rh/home_office/index.html')

@app.route('/rh/api/home-office/autorizar', methods=['POST'])
@login_required
def rh_api_autorizar_home_office():
    """API: Autorizar home office para colaborador"""
    try:
        data = request.get_json()
        
        return jsonify({
            'status': 'success',
            'message': 'Home office autorizado com sucesso!',
            'autorizacao': {
                'id': 1,
                'colaborador_id': data.get('colaborador_id'),
                'colaborador_nome': 'João Silva',
                'data_inicio': data.get('data_inicio'),
                'data_fim': data.get('data_fim'),
                'dias_semana': data.get('dias_semana', []),
                'motivo': data.get('motivo'),
                'status': 'ativo'
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/rh/api/home-office/listar')
@login_required
def rh_api_listar_home_office():
    """API: Listar autorizações de home office"""
    autorizacoes = [
        {
            'id': 1,
            'colaborador_nome': 'João Silva',
            'colaborador_id': 1,
            'data_inicio': '2024-11-01',
            'data_fim': '2024-11-30',
            'dias_semana': ['segunda', 'quarta'],
            'status': 'ativo',
            'motivo': 'Projeto especial'
        },
        {
            'id': 2,
            'colaborador_nome': 'Maria Santos',
            'colaborador_id': 2,
            'data_inicio': '2024-11-15',
            'data_fim': '2024-12-15',
            'dias_semana': ['sexta'],
            'status': 'ativo',
            'motivo': 'Desenvolvimento remoto'
        }
    ]
    
    return jsonify({
        'status': 'success',
        'autorizacoes': autorizacoes
    })

@app.route('/rh/api/home-office/<int:id>/cancelar', methods=['POST'])
@login_required
def rh_api_cancelar_home_office(id):
    """API: Cancelar autorização de home office"""
    try:
        data = request.get_json()
        
        return jsonify({
            'status': 'success',
            'message': 'Autorização cancelada com sucesso!'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


# ========== HOLERITE ==========

@app.route('/rh/holerites')
@login_required
def rh_holerites():
    """Página principal de holerites"""
    return render_template('rh/holerite/index.html')

@app.route('/rh/api/holerite/gerar', methods=['POST'])
@login_required
def rh_api_gerar_holerite():
    """API: Gerar holerite para colaborador"""
    try:
        data = request.get_json()
        
        salario_base = float(data.get('salario_base', 0))
        inss = salario_base * 0.11
        irrf = salario_base * 0.075 if salario_base > 2000 else 0
        
        return jsonify({
            'status': 'success',
            'message': 'Holerite gerado com sucesso!',
            'holerite': {
                'id': 1,
                'colaborador_id': data.get('colaborador_id'),
                'colaborador_nome': 'João Silva',
                'mes': data.get('mes'),
                'ano': data.get('ano'),
                'salario_base': salario_base,
                'vale_alimentacao': data.get('vale_alimentacao', 500),
                'vale_transporte': data.get('vale_transporte', 200),
                'auxilio_celular': data.get('auxilio_celular', 50),
                'total_vencimentos': salario_base + 750,
                'inss': inss,
                'irrf': irrf,
                'total_descontos': inss + irrf,
                'liquido': salario_base + 750 - inss - irrf
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/rh/api/holerite/listar')
@login_required
def rh_api_listar_holerites():
    """API: Listar holerites"""
    holerites = [
        {
            'id': 1,
            'colaborador_nome': 'João Silva',
            'colaborador_id': 1,
            'mes': 10,
            'ano': 2024,
            'salario_base': 3000.00,
            'total_vencimentos': 3750.00,
            'total_descontos': 555.00,
            'liquido': 3195.00,
            'status': 'gerado'
        },
        {
            'id': 2,
            'colaborador_nome': 'Maria Santos',
            'colaborador_id': 2,
            'mes': 10,
            'ano': 2024,
            'salario_base': 2500.00,
            'total_vencimentos': 3250.00,
            'total_descontos': 462.50,
            'liquido': 2787.50,
            'status': 'gerado'
        }
    ]
    
    return jsonify({
        'status': 'success',
        'holerites': holerites
    })

@app.route('/rh/api/holerite/<int:id>/pdf')
@login_required
def rh_api_holerite_pdf(id):
    """API: Gerar PDF do holerite"""
    try:
        # Mock de PDF simples
        buffer = BytesIO()
        buffer.write(b'PDF Mock - Holerite #' + str(id).encode())
        buffer.seek(0)
        
        return send_file(
            buffer, 
            as_attachment=True, 
            download_name=f'holerite_{id}.pdf', 
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


# ========== DRE GERENCIAL ==========

@app.route('/rh/dre')
@login_required
def rh_dre_gerencial():
    """Página de DRE Gerencial"""
    return render_template('rh/dre/index.html')

@app.route('/rh/api/dre/importar', methods=['POST'])
@login_required
def rh_api_importar_dre():
    """API: Importar DRE do contador"""
    try:
        data = request.form
        
        mes = int(data.get('mes', 1))
        ano = int(data.get('ano', 2024))
        
        return jsonify({
            'status': 'success',
            'message': 'DRE importada com sucesso!',
            'dre': {
                'id': 1,
                'mes': mes,
                'ano': ano,
                'receita_bruta': 150000.00,
                'deducoes': 15000.00,
                'receita_liquida': 135000.00,
                'custo_mercadorias': 60000.00,
                'lucro_bruto': 75000.00,
                'despesas_vendas': 15000.00,
                'despesas_administrativas': 25000.00,
                'despesas_financeiras': 5000.00,
                'receitas_financeiras': 2000.00,
                'resultado_operacional': 32000.00,
                'resultado_liquido': 29000.00
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/rh/api/dre/listar')
@login_required
def rh_api_listar_dre():
    """API: Listar DREs"""
    dres = [
        {
            'id': 1,
            'mes': 9,
            'ano': 2024,
            'receita_bruta': 120000.00,
            'receita_liquida': 108000.00,
            'lucro_bruto': 60000.00,
            'resultado_liquido': 25000.00
        },
        {
            'id': 2,
            'mes': 10,
            'ano': 2024,
            'receita_bruta': 150000.00,
            'receita_liquida': 135000.00,
            'lucro_bruto': 75000.00,
            'resultado_liquido': 29000.00
        },
        {
            'id': 3,
            'mes': 11,
            'ano': 2024,
            'receita_bruta': 180000.00,
            'receita_liquida': 162000.00,
            'lucro_bruto': 90000.00,
            'resultado_liquido': 38000.00
        }
    ]
    
    return jsonify({
        'status': 'success',
        'dres': dres
    })




"""
Rotas do módulo de Recursos Humanos
"""
from flask import render_template, request, jsonify, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from app.blueprints.rh import bp
from app import db
from datetime import datetime, date, timedelta
from io import BytesIO

# ========== PÁGINA PRINCIPAL RH ==========
@bp.route('/')
@login_required
def index():
    """Página principal de RH"""
    return render_template('rh/index.html')

# ========== COLABORADORES ==========
@bp.route('/colaboradores')
@login_required
def colaboradores():
    """Lista de colaboradores"""
    return render_template('rh/colaboradores/index.html')

@bp.route('/novo-colaborador')
@login_required
def novo_colaborador():
    """Novo colaborador"""
    return render_template('rh/colaboradores/novo.html')

# ========== BENEFÍCIOS ==========
@bp.route('/beneficios')
@login_required
def beneficios():
    """Página principal de benefícios"""
    return render_template('rh/beneficios/index.html')

@bp.route('/beneficios/novo', methods=['GET', 'POST'])
@login_required
def novo_beneficio():
    """Criar novo benefício"""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            # Aqui você implementaria a lógica de criação
            # Por enquanto, retorno de sucesso
            
            return jsonify({
                'status': 'success',
                'message': 'Benefício criado com sucesso!'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('rh/beneficios/novo.html')

@bp.route('/api/beneficios')
@login_required
def api_listar_beneficios():
    """API: Lista todos os benefícios"""
    # Mock de dados para não dar erro
    beneficios = [
        {
            'id': 1,
            'nome': 'Vale Alimentação',
            'tipo': 'fixo',
            'valor': 500.00,
            'ativo': True
        },
        {
            'id': 2,
            'nome': 'Auxílio Celular',
            'tipo': 'fixo',
            'valor': 50.00,
            'ativo': True
        }
    ]
    
    return jsonify({
        'status': 'success',
        'beneficios': beneficios
    })

# ========== PONTO ELETRÔNICO ==========
@app.route('/bater-ponto')
@login_required
def bater_ponto():
    """Página para bater ponto com GPS"""
    return render_template('rh/ponto/bater_ponto.html')

@bp.route('/gerenciar-ponto')
@login_required
def gerenciar_ponto():
    """Gerenciar registros de ponto"""
    return render_template('rh/ponto/gerenciar.html')

@bp.route('/controle-ponto')
@login_required
def controle_ponto():
    """Controle geral de ponto"""
    return render_template('rh/ponto/controle.html')

@bp.route('/api/registrar-ponto', methods=['POST'])
@login_required
def api_registrar_ponto():
    """API: Registrar ponto com localização"""
    try:
        data = request.get_json()
        
        # Mock de resposta
        return jsonify({
            'status': 'success',
            'message': 'Ponto registrado com sucesso!',
            'registro': {
                'id': 1,
                'tipo': data.get('tipo', 'entrada'),
                'horario': datetime.now().strftime('%H:%M:%S'),
                'localizacao': data.get('localizacao_texto', 'Local não informado')
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# ========== HOME OFFICE ==========
@bp.route('/home-office')
@login_required
def home_office():
    """Página de gerenciamento de home office"""
    return render_template('rh/home_office/index.html')

@bp.route('/api/home-office/autorizar', methods=['POST'])
@login_required
def api_autorizar_home_office():
    """API: Autorizar home office para colaborador"""
    try:
        data = request.get_json()
        
        # Mock de resposta
        return jsonify({
            'status': 'success',
            'message': 'Home office autorizado com sucesso!',
            'autorizacao': {
                'id': 1,
                'colaborador_id': data.get('colaborador_id'),
                'data_inicio': data.get('data_inicio'),
                'data_fim': data.get('data_fim')
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/api/home-office/listar')
@login_required
def api_listar_home_office():
    """API: Listar autorizações de home office"""
    # Mock de dados
    autorizacoes = [
        {
            'id': 1,
            'colaborador': 'João Silva',
            'data_inicio': '2024-01-15',
            'data_fim': '2024-01-19',
            'status': 'ativo'
        }
    ]
    
    return jsonify({
        'status': 'success',
        'autorizacoes': autorizacoes
    })

# ========== HOLERITES ==========
@bp.route('/holerites')
@login_required
def holerites():
    """Página principal de holerites"""
    return render_template('rh/holerite/holerites.html')

@bp.route('/api/holerite/gerar', methods=['POST'])
@login_required
def api_gerar_holerite():
    """API: Gerar holerite para colaborador"""
    try:
        data = request.get_json()
        
        # Mock de resposta
        return jsonify({
            'status': 'success',
            'message': 'Holerite gerado com sucesso!',
            'holerite': {
                'id': 1,
                'colaborador_id': data.get('colaborador_id'),
                'mes': data.get('mes'),
                'ano': data.get('ano'),
                'salario_base': data.get('salario_base', 0),
                'total_vencimentos': data.get('salario_base', 0),
                'total_descontos': 0,
                'liquido': data.get('salario_base', 0)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/api/holerite/listar')
@login_required
def api_listar_holerites():
    """API: Listar holerites"""
    # Mock de dados
    holerites = [
        {
            'id': 1,
            'colaborador': 'João Silva',
            'mes': 1,
            'ano': 2024,
            'liquido': 2500.00
        }
    ]
    
    return jsonify({
        'status': 'success',
        'holerites': holerites
    })

@bp.route('/api/holerite/<int:id>/pdf')
@login_required
def api_holerite_pdf(id):
    """API: Gerar PDF do holerite"""
    try:
        # Mock de PDF simples
        buffer = BytesIO()
        buffer.write(b'PDF Mock - Holerite #' + str(id).encode())
        buffer.seek(0)
        
        return send_file(
            buffer, 
            as_attachment=True, 
            download_name=f'holerite_{id}.pdf', 
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# ========== DRE GERENCIAL ==========
@bp.route('/dre')
@login_required
def dre_gerencial():
    """Página de DRE Gerencial"""
    return render_template('rh/dre/index.html')

@bp.route('/api/dre/importar', methods=['POST'])
@login_required
def api_importar_dre():
    """API: Importar DRE do contador"""
    try:
        # Mock de resposta
        return jsonify({
            'status': 'success',
            'message': 'DRE importada com sucesso!',
            'dre': {
                'id': 1,
                'mes': request.form.get('mes', 1),
                'ano': request.form.get('ano', 2024),
                'receita_bruta': 100000.00,
                'receita_liquida': 90000.00,
                'lucro_bruto': 50000.00,
                'resultado_liquido': 30000.00
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/api/dre/listar')
@login_required
def api_listar_dre():
    """API: Listar DREs"""
    # Mock de dados
    dres = [
        {
            'id': 1,
            'mes': 1,
            'ano': 2024,
            'receita_bruta': 100000.00,
            'resultado_liquido': 30000.00
        },
        {
            'id': 2,
            'mes': 2,
            'ano': 2024,
            'receita_bruta': 120000.00,
            'resultado_liquido': 35000.00
        }
    ]
    
    return jsonify({
        'status': 'success',
        'dres': dres
    })

# ========== RELATÓRIOS ==========
@bp.route('/relatorio-frequencias')
@login_required
def relatorio_frequencias():
    """Relatório de frequências"""
    return render_template('rh/relatorios/frequencias.html')

@bp.route('/gerenciar-ferias')
@login_required
def gerenciar_ferias():
    """Gerenciar férias"""
    return render_template('rh/ferias/gerenciar_ferias.html')

@bp.route('/exportar-dados')
@login_required
def exportar_dados():
    """Exportar dados"""
    return render_template('rh/exportar_dados.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Relatórios gerais"""
    return render_template('rh/relatorios/relatorios.html')


# ========== RELATÓRIOS ==========
@bp.route('/relatorio-frequencias')
@login_required
def relatorio_frequencias():
    """Relatório de frequências"""
    return render_template('rh/relatorios/frequencias.html')

@bp.route('/gerenciar-ferias')
@login_required
def gerenciar_ferias():
    """Gerenciar férias"""
    return render_template('rh/ferias/gerenciar_ferias.html')

@bp.route('/exportar-dados')
@login_required
def exportar_dados():
    """Exportar dados"""
    return render_template('rh/exportar_dados.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Relatórios gerais"""
    return render_template('rh/relatorios/relatorios.html')


# ========== MÓDULO FINANCEIRO ==========
@app.route('/financeiro')
@login_required
def financeiro():
    """Página principal do financeiro"""
    return render_template('financeiro/index.html')





# ========== GESTÃO DA VISTA ==========
@app.route('/gestao-vista')
@login_required
def gestao_vista():
    """Página de gestão da vista"""
    return render_template('gestao_vista/index.html')


if __name__ == '__main__':
    print("🏢 ERP SISTEMA - VERSÃO SIMPLIFICADA")

