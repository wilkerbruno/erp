from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.blueprints.gestao_vista import bp

@bp.route('/')
@login_required
def index():
    """Dashboard principal da Gestão à Vista"""
    return render_template('gestao_vista/index.html')

@bp.route('/indicadores')
@login_required
def indicadores():
    """Painel de Indicadores"""
    return render_template('gestao_vista/indicadores.html')

@bp.route('/metas')
@login_required
def metas():
    """Gestão de Metas e Objetivos"""
    return render_template('gestao_vista/metas.html')

@bp.route('/paineis')
@login_required
def paineis():
    """Painéis Visuais"""
    return render_template('gestao_vista/paineis.html')

@bp.route('/dashboards')
@login_required
def dashboards():
    """Dashboards Personalizados"""
    return render_template('gestao_vista/dashboards.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Relatórios Gerenciais"""
    return render_template('gestao_vista/relatorios.html')

# APIs
@bp.route('/api/indicador/criar', methods=['POST'])
@login_required
def api_criar_indicador():
    """API para criar novo indicador"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Indicador criado com sucesso!',
            'indicador_id': 123
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar indicador: {str(e)}'
        }), 500

@bp.route('/api/meta/atualizar/<int:meta_id>', methods=['PUT'])
@login_required
def api_atualizar_meta(meta_id):
    """API para atualizar meta"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': f'Meta {meta_id} atualizada com sucesso!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar meta: {str(e)}'
        }), 500
