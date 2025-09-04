from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.blueprints.planos import bp

@bp.route('/')
@login_required
def index():
    """Dashboard principal dos planos de ação"""
    return render_template('planos/index.html')

@bp.route('/novos')
@login_required
def novos_planos():
    """Lista de novos planos"""
    return render_template('planos/novos_planos.html')

@bp.route('/andamento')
@login_required
def planos_andamento():
    """Planos em andamento"""
    return render_template('planos/planos_andamento.html')

@bp.route('/kanban')
@login_required
def kanban_planos():
    """Visualização Kanban dos planos"""
    return render_template('planos/kanban_planos.html')

@bp.route('/novo')
@login_required
def novo_plano():
    """Criar novo plano de ação"""
    return render_template('planos/novo_plano.html')

@bp.route('/editar/<int:plano_id>')
@login_required
def editar_plano(plano_id):
    """Editar plano existente"""
    # Por enquanto redireciona para novo plano com dados pré-preenchidos
    return render_template('planos/novo_plano.html', plano_id=plano_id)

@bp.route('/visualizar/<int:plano_id>')
@login_required
def visualizar_plano(plano_id):
    """Visualizar detalhes do plano"""
    return render_template('planos/novos_planos.html', plano_id=plano_id)

# APIs para ações AJAX
@bp.route('/api/plano/aprovar/<int:plano_id>', methods=['POST'])
@login_required
def api_aprovar_plano(plano_id):
    """API para aprovar plano"""
    try:
        return jsonify({
            'success': True,
            'message': 'Plano {} aprovado com sucesso!'.format(plano_id)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao aprovar plano: {}'.format(str(e))
        }), 500

@bp.route('/api/plano/rejeitar/<int:plano_id>', methods=['POST'])
@login_required
def api_rejeitar_plano(plano_id):
    """API para rejeitar plano"""
    try:
        data = request.get_json()
        motivo = data.get('motivo', 'Sem motivo especificado')
        return jsonify({
            'success': True,
            'message': 'Plano {} rejeitado: {}'.format(plano_id, motivo)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao rejeitar plano: {}'.format(str(e))
        }), 500

@bp.route('/api/plano/status/<int:plano_id>', methods=['PUT'])
@login_required
def api_atualizar_status(plano_id):
    """API para atualizar status do plano"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        return jsonify({
            'success': True,
            'message': 'Status do plano {} atualizado para: {}'.format(plano_id, novo_status)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao atualizar status: {}'.format(str(e))
        }), 500

@bp.route('/api/plano/criar', methods=['POST'])
@login_required
def api_criar_plano():
    """API para criar novo plano"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Plano criado com sucesso!',
            'plano_id': 123  # Simular ID gerado
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao criar plano: {}'.format(str(e))
        }), 500
