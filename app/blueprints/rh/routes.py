from flask import render_template, request, jsonify
from flask_login import login_required
from app.blueprints.rh import bp
from datetime import datetime

@bp.route('/')
@login_required
def index():
    """Página principal do RH usando template"""
    return render_template('rh/index.html')

@bp.route('/colaboradores')
@login_required
def colaboradores():
    """Lista de colaboradores usando template"""
    return render_template('rh/colaboradores.html')

@bp.route('/novo-colaborador')
@login_required
def novo_colaborador():
    """Novo colaborador usando template"""
    return render_template('rh/novo_colaborador.html')

# === PÁGINAS DE PONTO COM TEMPLATES ===

@bp.route('/bater-ponto')
@login_required
def bater_ponto():
    """Bater ponto usando template"""
    return render_template('rh/bater_ponto.html')

@bp.route('/gerenciar-ponto')
@login_required
def gerenciar_ponto():
    """Gerenciar ponto usando template"""
    return render_template('rh/gerenciar_ponto.html')

@bp.route('/controle-ponto')
@login_required
def controle_ponto():
    """Controle de ponto usando template"""
    return render_template('rh/controle_ponto.html')

# === OUTRAS PÁGINAS BÁSICAS ===

@bp.route('/relatorio-frequencias')
@login_required
def relatorio_frequencias():
    """Relatório de frequências"""
    return render_template('rh/relatorio_frequencias.html')

@bp.route('/gerenciar-ferias')
@login_required
def gerenciar_ferias():
    """Gerenciar férias"""
    return render_template('rh/gerenciar_ferias.html')

@bp.route('/exportar-dados')
@login_required
def exportar_dados():
    """Exportar dados"""
    return render_template('rh/exportar_dados.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Página de relatórios"""
    return render_template('rh/relatorios.html')

@bp.route('/colaborador/<int:colaborador_id>')
@login_required
def ver_colaborador(colaborador_id):
    """Ver detalhes do colaborador"""
    colaborador = {
        'id': colaborador_id,
        'nome': 'João Silva',
        'cargo': 'Analista',
        'departamento': 'TI',
        'email': 'joao@empresa.com'
    }
    return render_template('rh/ver_colaborador.html', colaborador=colaborador)

@bp.route('/registrar-ponto-acao', methods=['POST'])
@login_required
def registrar_ponto_acao():
    """API para registrar ponto"""
    try:
        dados = request.get_json() if request.is_json else request.form.to_dict()
        tipo = dados.get('tipo', 'entrada')
        horario = dados.get('horario', datetime.now().strftime('%H:%M:%S'))
        
        return jsonify({
            'success': True,
            'message': f'Ponto de {tipo} registrado!',
            'horario': horario,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro: {str(e)}'
        })
