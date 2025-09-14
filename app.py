#!/usr/bin/env python3
"""
Aplicação Flask Simplificada para EasyPanel
Esta versão evita problemas de blueprints duplicados
"""

import os
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

if __name__ == '__main__':
    print("🏢 ERP SISTEMA - VERSÃO SIMPLIFICADA")
    print("="*50)
    print(f"🗄️  Database: {DATABASE_URL}")
    
    # Inicializar banco
    init_database()
    
    # Obter porta do ambiente
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 Iniciando servidor em {host}:{port}")
    print(f"🔗 Acesse: http://localhost:{port}")
    print(f"👤 Login: admin | 🔐 Senha: admin123")
    print("="*50)
    
    # Executar aplicação
    app.run(
        host=host,
        port=port,
        debug=False,
        threaded=True
    )