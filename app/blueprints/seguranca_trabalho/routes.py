from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.blueprints.seguranca_trabalho import bp

@bp.route('/')
@login_required
def index():
    """Dashboard principal da Segurança do Trabalho"""
    return render_template('seguranca_trabalho/index.html')

@bp.route('/acidentes')
@login_required
def acidentes():
    """Gestão de Acidentes e Incidentes"""
    return render_template('seguranca_trabalho/acidentes.html')

@bp.route('/treinamentos')
@login_required
def treinamentos():
    """Gestão de Treinamentos de Segurança"""
    return render_template('seguranca_trabalho/treinamentos.html')

@bp.route('/inspecoes')
@login_required
def inspecoes():
    """Inspeções e Auditorias de Segurança"""
    return render_template('seguranca_trabalho/inspecoes.html')

@bp.route('/epis')
@login_required
def epis():
    """Gestão de EPIs"""
    return render_template('seguranca_trabalho/epis.html')

@bp.route('/documentos')
@login_required
def documentos():
    """Documentos de Segurança"""
    return render_template('seguranca_trabalho/documentos.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Relatórios e Estatísticas"""
    return render_template('seguranca_trabalho/relatorios.html')

@bp.route('/novo-acidente')
@login_required
def novo_acidente():
    """Formulário para registrar novo acidente"""
    return render_template('seguranca_trabalho/novo_acidente.html')

@bp.route('/novo-treinamento')
@login_required
def novo_treinamento():
    """Formulário para criar novo treinamento"""
    return render_template('seguranca_trabalho/novo_treinamento.html')

@bp.route('/nova-inspecao')
@login_required
def nova_inspecao():
    """Formulário para nova inspeção"""
    return render_template('seguranca_trabalho/nova_inspecao.html')

# APIs
@bp.route('/api/acidente/criar', methods=['POST'])
@login_required
def api_criar_acidente():
    """API para criar novo registro de acidente"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Acidente registrado com sucesso!',
            'acidente_id': 123
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao registrar acidente: {str(e)}'
        }), 500

@bp.route('/api/treinamento/criar', methods=['POST'])
@login_required
def api_criar_treinamento():
    """API para criar novo treinamento"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Treinamento criado com sucesso!',
            'treinamento_id': 456
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar treinamento: {str(e)}'
        }), 500
