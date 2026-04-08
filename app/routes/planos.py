from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, csrf


@app.route('/planos-acao/')
@login_required
def planos_index():
    return render_template('planos/index.html')


@app.route('/planos-acao/novos')
@login_required
def planos_novos():
    return render_template('planos/novos_planos.html')


@app.route('/planos-acao/andamento')
@login_required
def planos_andamento():
    return render_template('planos/planos_andamento.html')


@app.route('/planos-acao/kanban')
@login_required
def planos_kanban():
    return render_template('planos/kanban_planos.html')


@app.route('/planos-acao/novo')
@login_required
def planos_novo():
    return render_template('planos/novo_plano.html')


@app.route('/planos-acao/editar/<int:plano_id>')
@login_required
def planos_editar(plano_id):
    return render_template('planos/novo_plano.html', plano_id=plano_id)


@app.route('/planos-acao/visualizar/<int:plano_id>')
@login_required
def planos_visualizar(plano_id):
    return render_template('planos/novos_planos.html', plano_id=plano_id)


@app.route('/planos-acao/api/plano/aprovar/<int:plano_id>', methods=['POST'])
@login_required
@csrf.exempt
def planos_api_aprovar(plano_id):
    try:
        return jsonify({
            'success': True,
            'message': f'Plano {plano_id} aprovado com sucesso!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/planos-acao/api/plano/rejeitar/<int:plano_id>', methods=['POST'])
@login_required
@csrf.exempt
def planos_api_rejeitar(plano_id):
    try:
        data = request.get_json()
        motivo = data.get('motivo', 'Sem motivo especificado')
        return jsonify({
            'success': True,
            'message': f'Plano {plano_id} rejeitado: {motivo}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/planos-acao/api/plano/status/<int:plano_id>', methods=['PUT'])
@login_required
@csrf.exempt
def planos_api_atualizar_status(plano_id):
    try:
        data = request.get_json()
        novo_status = data.get('status')
        return jsonify({
            'success': True,
            'message': f'Status do plano {plano_id} atualizado para: {novo_status}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/planos-acao/api/plano/criar', methods=['POST'])
@login_required
@csrf.exempt
def planos_api_criar():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Plano criado com sucesso!',
            'plano_id': 123
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500