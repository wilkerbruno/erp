#!/usr/bin/env python3
"""Run minimalista para testar"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# App simples
app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User:
    def __init__(self, username):
        self.username = username
        self.id = 1
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User('admin') if user_id == '1' else None

# Rotas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            user = User('admin')
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Credenciais invalidas', 'error')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h3 class="text-center">Login</h3>
                            <form method="POST">
                                <div class="mb-3">
                                    <input type="text" class="form-control" name="username" placeholder="Usuario" required>
                                </div>
                                <div class="mb-3">
                                    <input type="password" class="form-control" name="password" placeholder="Senha" required>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">Entrar</button>
                            </form>
                            <div class="text-center mt-3">
                                <small>admin / admin123</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/')
@login_required
def dashboard():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>Dashboard ERP</h1>
            <p>Bem-vindo, {current_user.username}!</p>
            <div class="row">
                <div class="col-md-3 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5>RH</h5>
                            <a href="/rh" class="btn btn-primary">Acessar</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5>Qualidade</h5>
                            <a href="/qualidade" class="btn btn-warning">Acessar</a>
                        </div>
                    </div>
                </div>
            </div>
            <a href="/logout" class="btn btn-secondary">Sair</a>
        </div>
    </body>
    </html>
    '''

@app.route('/rh')
@login_required
def rh():
    return '<h1>Modulo RH</h1><a href="/">Voltar</a>'

@app.route('/qualidade')
@login_required
def qualidade():
    return '<h1>Modulo Qualidade</h1><a href="/">Voltar</a>'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)