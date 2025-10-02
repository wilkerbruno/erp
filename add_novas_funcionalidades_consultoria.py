#!/usr/bin/env python3
"""
Adiciona apenas 4 novas funcionalidades ao módulo de consultoria EXISTENTE:
- Diagnóstico EFO
- Diagnóstico Inicial  
- Checklist SFM
- Acompanhamento

Mantém tudo que já existe funcionando!
"""

from pathlib import Path

def add_routes_to_existing_file():
    """Adiciona as 4 novas rotas ao arquivo de rotas existente"""
    
    route_file = Path("app/blueprints/consultoria/routes.py")
    
    if not route_file.exists():
        print("❌ Arquivo de rotas não encontrado em app/blueprints/consultoria/routes.py")
        return False
    
    # Ler conteúdo existente
    with open(route_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já existem as rotas
    if 'diagnostico_efo' in content:
        print("✅ Rotas já existem!")
        return True
    
    # Novas rotas para adicionar
    new_routes = '''
# ===== NOVAS FUNCIONALIDADES =====

@consultoria.route('/diagnostico-efo')
@login_required
def diagnostico_efo():
    """Diagnóstico EFO - Empresarial, Financeiro e Operacional"""
    return render_template('consultoria/diagnostico_efo.html')

@consultoria.route('/diagnostico-inicial')
@login_required
def diagnostico_inicial():
    """Diagnóstico Inicial - Checklist de Avaliação"""
    return render_template('consultoria/diagnostico_inicial.html')

@consultoria.route('/checklist-sfm')
@login_required
def checklist_sfm():
    """Checklist SFM - Shop Floor Management"""
    return render_template('consultoria/checklist_sfm.html')

@consultoria.route('/acompanhamento')
@login_required
def acompanhamento():
    """Acompanhamento - Auditorias e Follow-up"""
    return render_template('consultoria/acompanhamento.html')
'''
    
    # Adicionar as novas rotas antes do final do arquivo
    # Procurar por linhas em branco no final ou antes de outros blocos
    lines = content.split('\n')
    
    # Adicionar no final do arquivo, antes da última linha vazia
    insert_position = len(lines)
    
    # Inserir as novas rotas
    lines.insert(insert_position, new_routes)
    
    # Salvar arquivo atualizado
    updated_content = '\n'.join(lines)
    
    with open(route_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ 4 novas rotas adicionadas ao arquivo existente!")
    return True

def create_new_templates():
    """Cria apenas os 4 novos templates"""
    
    templates_dir = Path("app/templates/consultoria")
    
    if not templates_dir.exists():
        print("❌ Diretório de templates não encontrado!")
        return False
    
    # Template 1: Diagnóstico EFO
    diagnostico_efo = '''{% extends "base.html" %}

{% block title %}Diagnóstico EFO - Consultoria{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">
            <i class="fas fa-chart-pie me-2"></i>Diagnóstico EFO
        </h1>
        <div class="btn-group">
            <button class="btn btn-success" onclick="novoDiagnostico()">
                <i class="fas fa-plus me-1"></i>Novo Diagnóstico
            </button>
            <a href="{{ url_for('consultoria.index') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-1"></i>Voltar
            </a>
        </div>
    </div>

    <!-- Info EFO -->
    <div class="alert alert-info">
        <h5><i class="fas fa-info-circle me-2"></i>Diagnóstico EFO</h5>
        <p class="mb-0">Framework de avaliação Empresarial, Financeiro e Operacional para análise completa da organização.</p>
    </div>

    <!-- 3 Dimensões -->
    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card border-left-primary h-100">
                <div class="card-body text-center">
                    <i class="fas fa-building fa-3x text-primary mb-3"></i>
                    <h5 class="text-primary">Empresarial</h5>
                    <p class="text-muted">Estrutura, governança e estratégia</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-left-success h-100">
                <div class="card-body text-center">
                    <i class="fas fa-chart-line fa-3x text-success mb-3"></i>
                    <h5 class="text-success">Financeiro</h5>
                    <p class="text-muted">Análise financeira e rentabilidade</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-left-info h-100">
                <div class="card-body text-center">
                    <i class="fas fa-cogs fa-3x text-info mb-3"></i>
                    <h5 class="text-info">Operacional</h5>
                    <p class="text-muted">Processos e produtividade</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Lista de Diagnósticos -->
    <div class="card shadow">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">
                <i class="fas fa-list me-2"></i>Diagnósticos EFO
            </h6>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Cliente</th>
                            <th>Data</th>
                            <th>Status</th>
                            <th>Score</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>ABC Indústria</td>
                            <td>15/04/2024</td>
                            <td><span class="badge bg-success">Concluído</span></td>
                            <td>8.5</td>
                            <td>
                                <button class="btn btn-sm btn-primary"><i class="fas fa-eye"></i></button>
                                <button class="btn btn-sm btn-success"><i class="fas fa-file-pdf"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function novoDiagnostico() {
    alert('Criar novo Diagnóstico EFO');
}
console.log('Diagnóstico EFO carregado');
</script>
{% endblock %}'''

    # Template 2: Diagnóstico Inicial
    diagnostico_inicial = '''{% extends "base.html" %}

{% block title %}Diagnóstico Inicial - Consultoria{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">
            <i class="fas fa-clipboard-check me-2"></i>Diagnóstico Inicial
        </h1>
        <div class="btn-group">
            <button class="btn btn-success" onclick="novoChecklist()">
                <i class="fas fa-plus me-1"></i>Novo Checklist
            </button>
            <a href="{{ url_for('consultoria.index') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-1"></i>Voltar
            </a>
        </div>
    </div>

    <div class="alert alert-info">
        <h5><i class="fas fa-info-circle me-2"></i>Diagnóstico Inicial</h5>
        <p class="mb-0">Checklist completo de avaliação inicial para novos projetos de consultoria.</p>
    </div>

    <div class="card shadow">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">
                <i class="fas fa-list-check me-2"></i>Diagnósticos Iniciais
            </h6>
        </div>
        <div class="card-body">
            <div class="text-center py-5">
                <i class="fas fa-clipboard-check fa-5x text-muted mb-3"></i>
                <h4>Diagnóstico Inicial</h4>
                <p class="text-muted">Funcionalidade em desenvolvimento</p>
                <button class="btn btn-primary" onclick="novoChecklist()">
                    <i class="fas fa-plus me-2"></i>Começar
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function novoChecklist() {
    alert('Criar novo Diagnóstico Inicial');
}
console.log('Diagnóstico Inicial carregado');
</script>
{% endblock %}'''

    # Template 3: Checklist SFM
    checklist_sfm = '''{% extends "base.html" %}

{% block title %}Checklist SFM - Consultoria{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">
            <i class="fas fa-industry me-2"></i>Checklist SFM
        </h1>
        <div class="btn-group">
            <button class="btn btn-success" onclick="novoSFM()">
                <i class="fas fa-plus me-1"></i>Novo Checklist
            </button>
            <a href="{{ url_for('consultoria.index') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-1"></i>Voltar
            </a>
        </div>
    </div>

    <div class="alert alert-info">
        <h5><i class="fas fa-info-circle me-2"></i>Checklist SFM</h5>
        <p class="mb-0">Shop Floor Management - Gestão visual e acompanhamento de chão de fábrica.</p>
    </div>

    <div class="card shadow">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">
                <i class="fas fa-tasks me-2"></i>Checklists SFM
            </h6>
        </div>
        <div class="card-body">
            <div class="text-center py-5">
                <i class="fas fa-industry fa-5x text-muted mb-3"></i>
                <h4>Checklist SFM</h4>
                <p class="text-muted">Funcionalidade em desenvolvimento</p>
                <button class="btn btn-primary" onclick="novoSFM()">
                    <i class="fas fa-plus me-2"></i>Começar
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function novoSFM() {
    alert('Criar novo Checklist SFM');
}
console.log('Checklist SFM carregado');
</script>
{% endblock %}'''

    # Template 4: Acompanhamento
    acompanhamento = '''{% extends "base.html" %}

{% block title %}Acompanhamento - Consultoria{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">
            <i class="fas fa-search-plus me-2"></i>Acompanhamento
        </h1>
        <div class="btn-group">
            <button class="btn btn-success" onclick="novaAuditoria()">
                <i class="fas fa-plus me-1"></i>Nova Auditoria
            </button>
            <a href="{{ url_for('consultoria.index') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-1"></i>Voltar
            </a>
        </div>
    </div>

    <div class="alert alert-info">
        <h5><i class="fas fa-info-circle me-2"></i>Acompanhamento</h5>
        <p class="mb-0">Auditorias, follow-ups e acompanhamento de projetos de consultoria.</p>
    </div>

    <div class="card shadow">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">
                <i class="fas fa-calendar-check me-2"></i>Acompanhamentos
            </h6>
        </div>
        <div class="card-body">
            <div class="text-center py-5">
                <i class="fas fa-search-plus fa-5x text-muted mb-3"></i>
                <h4>Acompanhamento</h4>
                <p class="text-muted">Funcionalidade em desenvolvimento</p>
                <button class="btn btn-primary" onclick="novaAuditoria()">
                    <i class="fas fa-plus me-2"></i>Começar
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function novaAuditoria() {
    alert('Criar nova Auditoria');
}
console.log('Acompanhamento carregado');
</script>
{% endblock %}'''

    # Criar os templates
    templates = {
        'diagnostico_efo.html': diagnostico_efo,
        'diagnostico_inicial.html': diagnostico_inicial,
        'checklist_sfm.html': checklist_sfm,
        'acompanhamento.html': acompanhamento
    }
    
    created = []
    for filename, content in templates.items():
        filepath = templates_dir / filename
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            created.append(filename)
            print(f"   ✅ Criado: {filename}")
    
    if not created:
        print("   ✅ Todos os templates já existem")
    
    return True

def add_cards_to_index():
    """Adiciona os 4 novos cards ao index.html existente"""
    
    index_file = Path("app/templates/consultoria/index.html")
    
    if not index_file.exists():
        print("❌ Arquivo index.html não encontrado!")
        return False
    
    # Ler conteúdo existente
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já tem os cards
    if 'diagnostico-efo' in content:
        print("✅ Cards já existem no index!")
        return True
    
    # Novos cards para adicionar
    new_cards = '''
                <!-- Diagnóstico EFO -->
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card module-card h-100" onclick="acessarPagina('/consultoria/diagnostico-efo')">
                        <div class="card-body text-center">
                            <i class="fas fa-chart-pie fa-3x text-success mb-3"></i>
                            <h5>Diagnóstico EFO</h5>
                            <p class="text-muted">Empresarial, Financeiro e Operacional</p>
                            <button class="btn btn-success btn-sm">
                                <i class="fas fa-arrow-right me-1"></i>Acessar
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Diagnóstico Inicial -->
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card module-card h-100" onclick="acessarPagina('/consultoria/diagnostico-inicial')">
                        <div class="card-body text-center">
                            <i class="fas fa-clipboard-check fa-3x text-info mb-3"></i>
                            <h5>Diagnóstico Inicial</h5>
                            <p class="text-muted">Checklist de avaliação inicial</p>
                            <button class="btn btn-info btn-sm">
                                <i class="fas fa-arrow-right me-1"></i>Acessar
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Checklist SFM -->
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card module-card h-100" onclick="acessarPagina('/consultoria/checklist-sfm')">
                        <div class="card-body text-center">
                            <i class="fas fa-industry fa-3x text-warning mb-3"></i>
                            <h5>Checklist SFM</h5>
                            <p class="text-muted">Shop Floor Management</p>
                            <button class="btn btn-warning btn-sm">
                                <i class="fas fa-arrow-right me-1"></i>Acessar
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Acompanhamento -->
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card module-card h-100" onclick="acessarPagina('/consultoria/acompanhamento')">
                        <div class="card-body text-center">
                            <i class="fas fa-search-plus fa-3x text-danger mb-3"></i>
                            <h5>Acompanhamento</h5>
                            <p class="text-muted">Auditorias e follow-up</p>
                            <button class="btn btn-danger btn-sm">
                                <i class="fas fa-arrow-right me-1"></i>Acessar
                            </button>
                        </div>
                    </div>
                </div>
'''
    
    # Encontrar onde inserir (antes do fechamento do row dos cards)
    # Procurar pelo último card de "Relatórios"
    if "<!-- RELATÓRIOS - CORRIGIDO -->" in content:
        # Inserir depois do card de relatórios
        content = content.replace(
            '</div>\n            </div>\n        </div>\n    </div>',
            new_cards + '\n            </div>\n        </div>\n    </div>',
            1  # Apenas a primeira ocorrência
        )
    else:
        print("⚠️  Não foi possível encontrar o local exato para inserir os cards")
        print("   Você precisará adicionar manualmente")
        return False
    
    # Salvar arquivo atualizado
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 4 novos cards adicionados ao index!")
    return True

def main():
    """Executa a adição das funcionalidades"""
    
    print("🔧 ADICIONANDO 4 NOVAS FUNCIONALIDADES À CONSULTORIA")
    print("="*55)
    
    try:
        # 1. Adicionar rotas
        print("\n1. ➕ Adicionando rotas ao arquivo existente...")
        if not add_routes_to_existing_file():
            print("   ⚠️  Erro ao adicionar rotas")
            return False
        
        # 2. Criar templates
        print("\n2. 📄 Criando templates novos...")
        if not create_new_templates():
            print("   ⚠️  Erro ao criar templates")
            return False
        
        # 3. Atualizar index
        print("\n3. 🏠 Adicionando cards ao index...")
        if not add_cards_to_index():
            print("   ⚠️  Erro ao atualizar index")
            return False
        
        print(f"\n{'='*55}")
        print("✅ 4 NOVAS FUNCIONALIDADES ADICIONADAS COM SUCESSO!")
        
        print("\n📋 Funcionalidades adicionadas:")
        print("   1. Diagnóstico EFO - Empresarial, Financeiro e Operacional")
        print("   2. Diagnóstico Inicial - Checklist de avaliação")
        print("   3. Checklist SFM - Shop Floor Management")
        print("   4. Acompanhamento - Auditorias e follow-up")
        
        print("\n🔗 Novas URLs disponíveis:")
        print("   • /consultoria/diagnostico-efo")
        print("   • /consultoria/diagnostico-inicial")
        print("   • /consultoria/checklist-sfm")
        print("   • /consultoria/acompanhamento")
        
        print("\n🚀 Próximos passos:")
        print("   1. Reinicie o servidor Flask")
        print("   2. Acesse /consultoria")
        print("   3. Clique nos novos cards para testar")
        
        print("\n✨ O módulo existente foi mantido intacto!")
        print("   Apenas foram adicionados 4 novos cards e funcionalidades")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🎉 SUCESSO! 4 novas funcionalidades adicionadas!")
    else:
        print(f"\n💥 ERRO na adição das funcionalidades")