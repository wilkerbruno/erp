from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.blueprints.frotas import bp

@bp.route('/')
@login_required
def index():
    """Dashboard principal da Gestão à Vista"""
    return render_template('frotas/index.html')


# ========== MÓDULO FROTAS ==========

# Combustível
@bp.route('/combustivel')
@login_required
def frotas_combustivel():
    """Página de controle de combustível"""
    return render_template('frotas/combustivel/index.html')

@bp.route('/combustivel/registrar') 
@login_required
def frotas_registrar_combustivel():
    """Registrar abastecimento"""
    return render_template('frotas/combustivel/registrar.html')

# Documentação
@bp.route('/documentacao')
@login_required
def frotas_documentacao():
    """Página de documentação de veículos"""
    return render_template('frotas/documentacao/index.html')

@bp.route('/documentacao/alertas')
@login_required
def frotas_alertas_documentacao():
    """Alertas de documentação"""
    return render_template('frotas/documentacao/alertas.html')

# Manutenção
@bp.route('/manutencao')
@login_required
def frotas_manutencao():
    """Página de manutenção de veículos"""
    return render_template('frotas/manutencao/index.html')

@bp.route('/manutencao/agendar')
@login_required
def frotas_agendar_manutencao():
    """Agendar manutenção"""
    return render_template('frotas/manutencao/agendar.html')

# Motoristas
@bp.route('/motoristas')
@login_required
def frotas_motoristas():
    """Página de motoristas"""
    return render_template('frotas/motoristas/index.html')

@bp.route('/motoristas/novo')
@login_required
def frotas_novo_motorista():
    """Cadastrar novo motorista"""
    return render_template('frotas/motoristas/novo.html')

# Rastreamento
@bp.route('/rastreamento')
@login_required
def frotas_rastreamento():
    """Página de rastreamento"""
    return render_template('frotas/rastreamento/mapa.html')

@bp.route('/historico')
@login_required
def frotas_historico_rastreamento():
    """Histórico de rastreamento"""
    return render_template('frotas/rastreamento/historico.html')

@bp.route('/mapa')
@login_required
def frotas_mapa_rastreamento():
    """Mapa de rastreamento"""
    return render_template('frotas/rastreamento/mapa.html')

# Relatórios de Frotas
@bp.route('/relatorios')
@login_required
def frotas_relatorios():
    """Página de relatórios de frotas"""
    return render_template('frotas/relatorios/index.html')

@bp.route('/relatorios/custos')
@login_required
def frotas_relatorios_custos():
    """Relatório de custos"""
    return render_template('frotas/relatorios/custos.html')

@bp.route('/relatorios/geral')
@login_required
def frotas_relatorios_geral():
    """Relatório geral"""
    return render_template('frotas/relatorios/geral.html')

@bp.route('/relatorios/manutencao')
@login_required
def frotas_relatorios_manutencao():
    """Relatório de manutenção"""
    return render_template('frotas/relatorios/manutencao.html')

@bp.route('/relatorios/viagens')
@login_required
def frotas_relatorios_viagens():
    """Relatório de viagens"""
    return render_template('frotas/relatorios/viagens.html')

# Seguros
@bp.route('/seguros')
@login_required
def frotas_seguros():
    """Página de seguros"""
    return render_template('frotas/seguros/index.html')

# Veículos
@bp.route('/veiculos')
@login_required
def frotas_veiculos():
    """Página de veículos"""
    return render_template('frotas/veiculos/index.html')

@bp.route('/veiculos/detalhes/<int:veiculo_id>')
@login_required
def frotas_detalhes_veiculo(veiculo_id):
    """Detalhes do veículo"""
    return render_template('frotas/veiculos/detalhes.html', veiculo_id=veiculo_id)

@bp.route('/veiculos/novo')
@login_required
def frotas_novo_veiculo():
    """Cadastrar novo veículo"""
    return render_template('frotas/veiculos/novo.html')


# ========== MÓDULO VIAGENS ==========
@bp.route('/viagens')
@login_required
def viagens():
    """Página principal de viagens"""
    return render_template('viagens/index.html')

@bp.route('/viagens/nova')
@login_required
def viagens_nova():
    """Cadastrar nova viagem"""
    return render_template('viagens/nova.html')

@bp.route('/viagens/editar/<int:viagem_id>')
@login_required
def viagens_editar(viagem_id):
    """Editar viagem"""
    return render_template('viagens/editar.html', viagem_id=viagem_id)