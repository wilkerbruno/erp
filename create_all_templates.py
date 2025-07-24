#!/usr/bin/env python3
"""
Script para criar todos os templates completos
"""

import os
from pathlib import Path

def create_rh_templates():
    """Cria templates do módulo RH"""
    print("Criando templates RH...")
    
    rh_dir = Path("app/templates/rh")
    rh_dir.mkdir(parents=True, exist_ok=True)
    
    # Lista de colaboradores
    colaboradores_content = """{% extends "base.html" %}

{% block title %}Recursos Humanos - Colaboradores{% endblock %}

{% block content %}
<div class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="h3 mb-0 text-gray-800">
        <i class="fas fa-users me-2"></i>Gestão de Colaboradores
    </h1>
    <div>
        <button class="btn btn-primary btn-sm" onclick="novoColaborador()">
            <i class="fas fa-plus me-1"></i>Novo Colaborador
        </button>
        <button class="btn btn-outline-primary btn-sm" onclick="exportarDados()">
            <i class="fas fa-download me-1"></i>Exportar
        </button>
    </div>
</div>

<!-- Statistics Cards -->
<div class="row mb-4">
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                            Total Colaboradores
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">156</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-users fa-2x text-gray-300"></i>
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
                            Ativos
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">148</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-user-check fa-2x text-gray-300"></i>
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
                            Admissões (Mês)
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">8</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-user-plus fa-2x text-gray-300"></i>
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
                            Turnover (%)
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">2.5%</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-chart-line fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Filtros -->
<div class="card shadow mb-4">
    <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Filtros e Busca</h6>
    </div>
    <div class="card-body">
        <div class="row">
            <div class="col-md-3">
                <div class="form-group">
                    <label for="buscarNome">Nome/Matrícula</label>
                    <input type="text" class="form-control" id="buscarNome" placeholder="Buscar colaborador...">
                </div>
            </div>
            <div class="col-md-2">
                <div class="form-group">
                    <label for="filtroSetor">Setor</label>
                    <select class="form-select" id="filtroSetor">
                        <option value="">Todos</option>
                        <option value="producao">Produção</option>
                        <option value="administrativo">Administrativo</option>
                        <option value="vendas">Vendas</option>
                        <option value="rh">RH</option>
                    </select>
                </div>
            </div>
            <div class="col-md-2">
                <div class="form-group">
                    <label for="filtroStatus">Status</label>
                    <select class="form-select" id="filtroStatus">
                        <option value="">Todos</option>
                        <option value="ativo">Ativo</option>
                        <option value="inativo">Inativo</option>
                        <option value="ferias">Férias</option>
                        <option value="afastado">Afastado</option>
                    </select>
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label for="filtroCargo">Cargo</label>
                    <select class="form-select" id="filtroCargo">
                        <option value="">Todos</option>
                        <option value="operador">Operador</option>
                        <option value="supervisor">Supervisor</option>
                        <option value="gerente">Gerente</option>
                        <option value="diretor">Diretor</option>
                    </select>
                </div>
            </div>
            <div class="col-md-2">
                <div class="form-group">
                    <label>&nbsp;</label>
                    <button class="btn btn-primary d-block" onclick="aplicarFiltros()">
                        <i class="fas fa-search"></i> Filtrar
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Lista de Colaboradores -->
<div class="card shadow">
    <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Lista de Colaboradores</h6>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-bordered" width="100%" cellspacing="0">
                <thead>
                    <tr>
                        <th>Foto</th>
                        <th>Matrícula</th>
                        <th>Nome</th>
                        <th>Cargo</th>
                        <th>Setor</th>
                        <th>Admissão</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <img src="https://via.placeholder.com/40x40" class="rounded-circle" alt="Foto">
                        </td>
                        <td>COL000001</td>
                        <td><strong>João Silva Santos</strong><br><small class="text-muted">joao.silva@empresa.com</small></td>
                        <td>Gerente de Produção</td>
                        <td><span class="badge bg-primary">Produção</span></td>
                        <td>15/03/2020</td>
                        <td><span class="badge bg-success">Ativo</span></td>
                        <td>
                            <div class="btn-group" role="group">
                                <button class="btn btn-sm btn-info" onclick="verColaborador(1)">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-sm btn-warning" onclick="editarColaborador(1)">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-secondary" onclick="historicoColaborador(1)">
                                    <i class="fas fa-history"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <img src="https://via.placeholder.com/40x40" class="rounded-circle" alt="Foto">
                        </td>
                        <td>COL000002</td>
                        <td><strong>Maria Santos Lima</strong><br><small class="text-muted">maria.santos@empresa.com</small></td>
                        <td>Supervisora de Qualidade</td>
                        <td><span class="badge bg-warning">Qualidade</span></td>
                        <td>22/08/2019</td>
                        <td><span class="badge bg-success">Ativo</span></td>
                        <td>
                            <div class="btn-group" role="group">
                                <button class="btn btn-sm btn-info" onclick="verColaborador(2)">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-sm btn-warning" onclick="editarColaborador(2)">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-secondary" onclick="historicoColaborador(2)">
                                    <i class="fas fa-history"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <img src="https://via.placeholder.com/40x40" class="rounded-circle" alt="Foto">
                        </td>
                        <td>COL000003</td>
                        <td><strong>Pedro Costa Oliveira</strong><br><small class="text-muted">pedro.costa@empresa.com</small></td>
                        <td>Operador de Máquina</td>
                        <td><span class="badge bg-primary">Produção</span></td>
                        <td>10/01/2022</td>
                        <td><span class="badge bg-info">Férias</span></td>
                        <td>
                            <div class="btn-group" role="group">
                                <button class="btn btn-sm btn-info" onclick="verColaborador(3)">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-sm btn-warning" onclick="editarColaborador(3)">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-secondary" onclick="historicoColaborador(3)">
                                    <i class="fas fa-history"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Paginação -->
        <div class="d-flex justify-content-between align-items-center mt-3">
            <div>
                <small class="text-muted">Mostrando 1 a 3 de 156 registros</small>
            </div>
            <nav>
                <ul class="pagination pagination-sm mb-0">
                    <li class="page-item disabled">
                        <span class="page-link">Anterior</span>
                    </li>
                    <li class="page-item active">
                        <span class="page-link">1</span>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="#">2</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="#">3</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="#">Próximo</a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function novoColaborador() {
    alert('Funcionalidade em desenvolvimento: Novo Colaborador');
}

function verColaborador(id) {
    alert('Visualizando colaborador ID: ' + id);
}

function editarColaborador(id) {
    alert('Editando colaborador ID: ' + id);
}

function historicoColaborador(id) {
    alert('Histórico do colaborador ID: ' + id);
}

function aplicarFiltros() {
    alert('Aplicando filtros...');
}

function exportarDados() {
    alert('Exportando dados...');
}
</script>
{% endblock %}
"""
    
    with open(rh_dir / "colaboradores.html", 'w', encoding='utf-8') as f:
        f.write(colaboradores_content)
    
    # Index RH
    index_content = """{% extends "base.html" %}

{% block title %}Recursos Humanos{% endblock %}

{% block content %}
<div class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="h3 mb-0 text-gray-800">
        <i class="fas fa-users me-2"></i>Recursos Humanos
    </h1>
</div>

<div class="row">
    <div class="col-lg-6 col-md-12 mb-4">
        <div class="card shadow h-100">
            <div class="card-header">
                <h6 class="m-0 font-weight-bold text-primary">Gestão de Colaboradores</h6>
            </div>
            <div class="card-body">
                <p>Gerencie todos os colaboradores da empresa.</p>
                <a href="/rh/colaboradores" class="btn btn-primary">Acessar Colaboradores</a>
            </div>
        </div>
    </div>
    
    <div class="col-lg-6 col-md-12 mb-4">
        <div class="card shadow h-100">
            <div class="card-header">
                <h6 class="m-0 font-weight-bold text-primary">Ponto Eletrônico</h6>
            </div>
            <div class="card-body">
                <p>Controle de ponto e frequência dos colaboradores.</p>
                <button class="btn btn-info" onclick="alert('Em desenvolvimento')">Em Breve</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
    
    with open(rh_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("✅ Templates RH criados!")

def create_qualidade_templates():
    """Cria templates do módulo Qualidade"""
    print("Criando templates Qualidade...")
    
    qual_dir = Path("app/templates/qualidade")
    qual_dir.mkdir(parents=True, exist_ok=True)
    
    # Não conformidades
    nc_content = """{% extends "base.html" %}

{% block title %}Qualidade - Não Conformidades{% endblock %}

{% block content %}
<div class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="h3 mb-0 text-gray-800">
        <i class="fas fa-exclamation-triangle me-2"></i>Não Conformidades
    </h1>
    <div>
        <button class="btn btn-primary btn-sm" onclick="novaNC()">
            <i class="fas fa-plus me-1"></i>Nova NC
        </button>
        <button class="btn btn-outline-primary btn-sm" onclick="exportarNCs()">
            <i class="fas fa-download me-1"></i>Exportar
        </button>
    </div>
</div>

<!-- Statistics Cards -->
<div class="row mb-4">
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-danger shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">
                            NCs Abertas
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">8</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-exclamation-circle fa-2x text-gray-300"></i>
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
                            Em Tratamento
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">15</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-tools fa-2x text-gray-300"></i>
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
                            Fechadas (Mês)
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">42</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-check-circle fa-2x text-gray-300"></i>
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
                            Taxa Resolução
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">94%</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-chart-line fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Lista de NCs -->
<div class="card shadow">
    <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Não Conformidades Recentes</h6>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-bordered" width="100%" cellspacing="0">
                <thead>
                    <tr>
                        <th>Número</th>
                        <th>Título</th>
                        <th>Origem</th>
                        <th>Criticidade</th>
                        <th>Responsável</th>
                        <th>Data Abertura</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>NC20250001</strong></td>
                        <td>Produto fora de especificação</td>
                        <td><span class="badge bg-primary">Interno</span></td>
                        <td><span class="badge bg-danger">Alta</span></td>
                        <td>João Silva</td>
                        <td>20/01/2025</td>
                        <td><span class="badge bg-warning">Em Tratamento</span></td>
                        <td>
                            <div class="btn-group" role="group">
                                <button class="btn btn-sm btn-info" onclick="verNC(1)">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-sm btn-warning" onclick="editarNC(1)">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><strong>NC20250002</strong></td>
                        <td>Atraso na entrega</td>
                        <td><span class="badge bg-success">Cliente</span></td>
                        <td><span class="badge bg-warning">Média</span></td>
                        <td>Maria Santos</td>
                        <td>18/01/2025</td>
                        <td><span class="badge bg-success">Fechada</span></td>
                        <td>
                            <div class="btn-group" role="group">
                                <button class="btn btn-sm btn-info" onclick="verNC(2)">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="btn btn-sm btn-secondary" onclick="reabrirNC(2)">
                                    <i class="fas fa-redo"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function novaNC() {
    alert('Funcionalidade em desenvolvimento: Nova NC');
}

function verNC(id) {
    alert('Visualizando NC ID: ' + id);
}

function editarNC(id) {
    alert('Editando NC ID: ' + id);
}

function reabrirNC(id) {
    if(confirm('Deseja reabrir esta NC?')) {
        alert('NC ' + id + ' reaberta!');
    }
}

function exportarNCs() {
    alert('Exportando NCs...');
}
</script>
{% endblock %}
"""
    
    with open(qual_dir / "nao_conformidades.html", 'w', encoding='utf-8') as f:
        f.write(nc_content)
    
    print("✅ Templates Qualidade criados!")

def create_remaining_templates():
    """Cria templates para os módulos restantes"""
    print("Criando templates restantes...")
    
    modules_data = {
        'producao': {
            'title': 'Produção (PCP)',
            'icon': 'fas fa-industry',
            'color': 'primary',
            'items': [
                {'name': 'Ordens de Produção', 'desc': 'Controle de ordens de produção'},
                {'name': 'Produtos', 'desc': 'Cadastro de produtos'},
                {'name': 'OEE', 'desc': 'Overall Equipment Effectiveness'},
            ]
        },
        'compras': {
            'title': 'Compras & Estoque', 
            'icon': 'fas fa-shopping-cart',
            'color': 'info',
            'items': [
                {'name': 'Ordens de Compra', 'desc': 'Gestão de compras'},
                {'name': 'Fornecedores', 'desc': 'Cadastro de fornecedores'},
                {'name': 'Estoque', 'desc': 'Controle de estoque'},
            ]
        },
        'planos_acao': {
            'title': 'Planos de Ação',
            'icon': 'fas fa-tasks', 
            'color': 'success',
            'items': [
                {'name': 'Novos Planos', 'desc': 'Criar planos de ação'},
                {'name': 'Em Andamento', 'desc': 'Planos em execução'},
                {'name': 'Kanban', 'desc': 'Visualização Kanban'},
            ]
        },
        'consultoria': {
            'title': 'Consultoria',
            'icon': 'fas fa-handshake',
            'color': 'warning', 
            'items': [
                {'name': 'Projetos', 'desc': 'Projetos de consultoria'},
                {'name': 'Clientes', 'desc': 'Gestão de clientes'},
                {'name': 'Produtos', 'desc': 'Produtos de consultoria'},
            ]
        },
        'financeiro': {
            'title': 'Financeiro',
            'icon': 'fas fa-dollar-sign',
            'color': 'success',
            'items': [
                {'name': 'DRE Gerencial', 'desc': 'Demonstrativo de resultados'},
                {'name': 'Contas a Pagar', 'desc': 'Gestão de pagamentos'},
                {'name': 'Contas a Receber', 'desc': 'Gestão de recebimentos'},
            ]
        },
        'manutencao': {
            'title': 'Manutenção',
            'icon': 'fas fa-tools',
            'color': 'secondary',
            'items': [
                {'name': 'Equipamentos', 'desc': 'Cadastro de equipamentos'},
                {'name': 'Ordens de Serviço', 'desc': 'Manutenções programadas'},
                {'name': 'Planos de Manutenção', 'desc': 'Planejamento de manutenções'},
            ]
        },
        'projetos': {
            'title': 'Gestão de Projetos',
            'icon': 'fas fa-project-diagram',
            'color': 'primary',
            'items': [
                {'name': 'Portfólio', 'desc': 'Visão geral dos projetos'},
                {'name': 'Cronograma', 'desc': 'Cronograma de projetos'},
                {'name': 'Recursos', 'desc': 'Gestão de recursos'},
            ]
        },
        'relatorios': {
            'title': 'Relatórios e Analytics',
            'icon': 'fas fa-chart-bar',
            'color': 'info',
            'items': [
                {'name': 'Dashboard Executivo', 'desc': 'Visão executiva'},
                {'name': 'Relatórios Operacionais', 'desc': 'Relatórios detalhados'},
                {'name': 'Indicadores', 'desc': 'KPIs e métricas'},
            ]
        }
    }
    
    for module, data in modules_data.items():
        module_dir = Path(f"app/templates/{module}")
        module_dir.mkdir(parents=True, exist_ok=True)
        
        index_content = f"""{{%extends "base.html" %}}

{{%block title %}}{data['title']}{{%endblock %}}

{{%block content %}}
<div class="d-sm-flex align-items-center justify-content-between mb-4">
    <h1 class="h3 mb-0 text-gray-800">
        <i class="{data['icon']} me-2"></i>{data['title']}
    </h1>
    <div>
        <button class="btn btn-{data['color']} btn-sm" onclick="novaAcao()">
            <i class="fas fa-plus me-1"></i>Novo
        </button>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="alert alert-{data['color']}" role="alert">
            <h4 class="alert-heading"><i class="{data['icon']} me-2"></i>Módulo {data['title']}</h4>
            <p>Este módulo está em desenvolvimento ativo. As funcionalidades principais incluem:</p>
            <hr>
            <ul class="mb-0">
"""
        
        for item in data['items']:
            index_content += f"""                <li><strong>{item['name']}</strong> - {item['desc']}</li>\n"""
        
        index_content += f"""            </ul>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-lg-4 mb-4">
        <div class="card border-left-{data['color']} shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-{data['color']} text-uppercase mb-1">
                            Status
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">Em Desenvolvimento</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-code fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-lg-4 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                            Previsão
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">Próxima Versão</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-calendar fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-lg-4 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
            <div class="card-body">
                <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                        <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                            Funcionalidades
                        </div>
                        <div class="h5 mb-0 font-weight-bold text-gray-800">{len(data['items'])}</div>
                    </div>
                    <div class="col-auto">
                        <i class="fas fa-list fa-2x text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="card shadow">
    <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Funcionalidades Disponíveis</h6>
    </div>
    <div class="card-body">
        <div class="row">
"""
        
        for i, item in enumerate(data['items']):
            index_content += f"""            <div class="col-md-4 mb-3">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <i class="{data['icon']} fa-2x text-{data['color']} mb-3"></i>
                        <h5>{item['name']}</h5>
                        <p class="text-muted">{item['desc']}</p>
                        <button class="btn btn-{data['color']} btn-sm" onclick="acessarFuncionalidade('{item['name']}')">
                            Em Breve
                        </button>
                    </div>
                </div>
            </div>
"""
        
        index_content += """        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function novaAcao() {
    alert('Funcionalidade em desenvolvimento');
}

function acessarFuncionalidade(nome) {
    alert('Funcionalidade "' + nome + '" será disponibilizada em breve!');
}
</script>
{% endblock %}
"""
        
        with open(module_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    print("✅ Templates restantes criados!")

def main():
    print("🎨 CRIANDO TODOS OS TEMPLATES COMPLETOS")
    print("="*50)
    
    create_rh_templates()
    create_qualidade_templates() 
    create_remaining_templates()
    
    print("="*50)
    print("✅ TODOS OS TEMPLATES CRIADOS!")
    print("📋 Módulos disponíveis:")
    print("  - RH (Colaboradores completo)")
    print("  - Qualidade (NCs completo)")
    print("  - Produção, Compras, Planos de Ação")
    print("  - Consultoria, Financeiro, Manutenção")
    print("  - Projetos, Relatórios")
    print("="*50)

if __name__ == "__main__":
    main()