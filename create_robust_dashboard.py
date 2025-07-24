#!/usr/bin/env python3
"""
Cria dashboard robusto que não quebra
"""

import os
from pathlib import Path

def create_safe_dashboard_template():
    """Cria template dashboard super seguro"""
    print("Criando dashboard super seguro...")
    
    dashboard_dir = Path("app/templates/dashboard")
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    
    # Template super simples que não pode quebrar
    dashboard_content = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - ERP Corrigindo à Rota</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Nunito', sans-serif;
            background-color: #f8f9fc;
        }
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card {
            border: none;
            border-radius: 10px;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
        }
        .module-card {
            transition: transform 0.2s;
            cursor: pointer;
        }
        .module-card:hover {
            transform: translateY(-5px);
        }
        .border-left-primary { border-left: 0.25rem solid #4e73df !important; }
        .border-left-success { border-left: 0.25rem solid #1cc88a !important; }
        .border-left-info { border-left: 0.25rem solid #36b9cc !important; }
        .border-left-warning { border-left: 0.25rem solid #f6c23e !important; }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fas fa-route me-2"></i>ERP Corrigindo à Rota
            </a>
            <div class="navbar-nav ms-auto">
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        <i class="fas fa-user me-1"></i>
                        {% if current_user.is_authenticated %}
                            {{ current_user.username|title }}
                        {% else %}
                            Usuário
                        {% endif %}
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="/auth/logout">
                            <i class="fas fa-sign-out-alt me-2"></i>Sair
                        </a></li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container-fluid mt-4">
        <!-- Header -->
        <div class="d-sm-flex align-items-center justify-content-between mb-4">
            <h1 class="h3 mb-0 text-gray-800">
                <i class="fas fa-tachometer-alt me-2"></i>Dashboard
            </h1>
            <div>
                <span class="text-muted">
                    <i class="fas fa-clock me-1"></i>
                    <span id="current-time"></span>
                </span>
            </div>
        </div>

        <!-- Alert de Sucesso -->
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <h4 class="alert-heading">
                <i class="fas fa-check-circle me-2"></i>Sistema Funcionando!
            </h4>
            <p>Bem-vindo ao ERP Corrigindo à Rota. O sistema está operacional e pronto para uso.</p>
            <hr>
            <p class="mb-0">
                <strong>Usuário:</strong> 
                {% if current_user.is_authenticated %}
                    {{ current_user.username|title }}
                {% else %}
                    Não identificado
                {% endif %}
                | <strong>Versão:</strong> 1.0.0
            </p>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>

        <!-- Statistics Cards -->
        <div class="row mb-4">
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-primary shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                    Status do Sistema
                                </div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">Online</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-server fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-success shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                    Módulos Ativos
                                </div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">8</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-puzzle-piece fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-info shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                                    Última Atualização
                                </div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">Hoje</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-clock fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-xl-3 col-md-6 mb-4">
                <div class="card border-left-warning shadow h-100 py-2">
                    <div class="card-body">
                        <div class="row no-gutters align-items-center">
                            <div class="col mr-2">
                                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                    Versão
                                </div>
                                <div class="h5 mb-0 font-weight-bold text-gray-800">1.0.0</div>
                            </div>
                            <div class="col-auto">
                                <i class="fas fa-code-branch fa-2x text-gray-300"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Módulos -->
        <div class="card shadow">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">
                    <i class="fas fa-th-large me-2"></i>Módulos do Sistema
                </h6>
            </div>
            <div class="card-body">
                <div class="row">
                    <!-- RH -->
                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/rh')">
                            <div class="card-body text-center">
                                <i class="fas fa-users fa-3x text-info mb-3"></i>
                                <h5>Recursos Humanos</h5>
                                <p class="text-muted">Gestão de colaboradores</p>
                                <button class="btn btn-info btn-sm">
                                    <i class="fas fa-arrow-right me-1"></i>Acessar
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Qualidade -->
                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/qualidade')">
                            <div class="card-body text-center">
                                <i class="fas fa-award fa-3x text-warning mb-3"></i>
                                <h5>Qualidade</h5>
                                <p class="text-muted">NCs e auditorias</p>
                                <button class="btn btn-warning btn-sm">
                                    <i class="fas fa-arrow-right me-1"></i>Acessar
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Produção -->
                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/producao')">
                            <div class="card-body text-center">
                                <i class="fas fa-industry fa-3x text-primary mb-3"></i>
                                <h5>Produção</h5>
                                <p class="text-muted">PCP e controle</p>
                                <button class="btn btn-primary btn-sm">
                                    <i class="fas fa-arrow-right me-1"></i>Acessar
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Planos de Ação -->
                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/planos-acao')">
                            <div class="card-body text-center">
                                <i class="fas fa-tasks fa-3x text-success mb-3"></i>
                                <h5>Planos de Ação</h5>
                                <p class="text-muted">5W2H e melhorias</p>
                                <button class="btn btn-success btn-sm">
                                    <i class="fas fa-arrow-right me-1"></i>Acessar
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Outros módulos -->
                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/compras')">
                            <div class="card-body text-center">
                                <i class="fas fa-shopping-cart fa-3x text-info mb-3"></i>
                                <h5>Compras</h5>
                                <p class="text-muted">Gestão de compras</p>
                                <button class="btn btn-info btn-sm">Em Breve</button>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/financeiro')">
                            <div class="card-body text-center">
                                <i class="fas fa-dollar-sign fa-3x text-success mb-3"></i>
                                <h5>Financeiro</h5>
                                <p class="text-muted">DRE e controle</p>
                                <button class="btn btn-success btn-sm">Em Breve</button>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/relatorios')">
                            <div class="card-body text-center">
                                <i class="fas fa-chart-bar fa-3x text-secondary mb-3"></i>
                                <h5>Relatórios</h5>
                                <p class="text-muted">Analytics e KPIs</p>
                                <button class="btn btn-secondary btn-sm">Em Breve</button>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-3 col-md-6 mb-4">
                        <div class="card module-card h-100" onclick="acessarModulo('/configuracoes')">
                            <div class="card-body text-center">
                                <i class="fas fa-cogs fa-3x text-dark mb-3"></i>
                                <h5>Configurações</h5>
                                <p class="text-muted">Configurações gerais</p>
                                <button class="btn btn-dark btn-sm">Em Breve</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Atualizar horário
        function updateTime() {
            const now = new Date();
            const timeString = now.toLocaleTimeString('pt-BR');
            const dateString = now.toLocaleDateString('pt-BR');
            document.getElementById('current-time').textContent = dateString + ' ' + timeString;
        }
        
        // Acessar módulo
        function acessarModulo(url) {
            window.location.href = url;
        }
        
        // Inicializar
        document.addEventListener('DOMContentLoaded', function() {
            updateTime();
            setInterval(updateTime, 1000);
            
            // Auto-hide alerts
            setTimeout(function() {
                var alerts = document.querySelectorAll('.alert-dismissible');
                alerts.forEach(function(alert) {
                    var alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
                    alertInstance.close();
                });
            }, 10000);
        });
        
        console.log('Dashboard carregado com sucesso!');
    </script>
</body>
</html>
"""
    
    with open(dashboard_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(dashboard_content)
    
    print("✅ Dashboard super seguro criado!")

def create_safe_dashboard_routes():
    """Cria rotas dashboard super seguras"""
    print("Criando rotas dashboard seguras...")
    
    dashboard_routes = """from flask import render_template
from flask_login import login_required, current_user
from app.blueprints.dashboard import bp

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    try:
        # Renderizar template de forma super segura
        return render_template('dashboard/index.html')
    except Exception as e:
        # Fallback se der erro
        return f'''
        <h1>Dashboard - Sistema Funcionando!</h1>
        <p>Bem-vindo ao ERP!</p>
        <p>Usuário: {current_user.username if current_user.is_authenticated else "Desconhecido"}</p>
        <p><a href="/rh">RH</a> | <a href="/qualidade">Qualidade</a> | <a href="/auth/logout">Sair</a></p>
        <p>Erro: {str(e)}</p>
        '''
"""
    
    dashboard_dir = Path("app/blueprints/dashboard")
    with open(dashboard_dir / "routes.py", 'w', encoding='utf-8') as f:
        f.write(dashboard_routes)
    
    print("✅ Rotas dashboard seguras criadas!")

def main():
    print("🛡️  CRIANDO DASHBOARD SUPER ROBUSTO")
    print("="*50)
    
    create_safe_dashboard_template()
    create_safe_dashboard_routes()
    
    print("="*50)
    print("✅ DASHBOARD ROBUSTO CRIADO!")
    print("Execute: python debug_error_500.py")
    print("Depois: python run.py")
    print("="*50)

if __name__ == "__main__":
    main()