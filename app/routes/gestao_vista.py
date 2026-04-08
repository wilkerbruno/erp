from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, csrf


@app.route('/gestao-vista/')
@login_required
def gestao_vista_index():
    return render_template('gestao_vista/index.html')


@app.route('/gestao-vista/indicadores')
@login_required
def gestao_vista_indicadores():
    return render_template('gestao_vista/indicadores.html')


@app.route('/gestao-vista/metas')
@login_required
def gestao_vista_metas():
    return render_template('gestao_vista/metas.html')


@app.route('/gestao-vista/paineis')
@login_required
def gestao_vista_paineis():
    return render_template('gestao_vista/paineis.html')


@app.route('/gestao-vista/dashboards')
@login_required
def gestao_vista_dashboards():
    return render_template('gestao_vista/dashboards.html')


@app.route('/gestao-vista/relatorios')
@login_required
def gestao_vista_relatorios():
    return render_template('gestao_vista/relatorios.html')


@app.route('/gestao-vista/api/indicador/criar', methods=['POST'])
@login_required
@csrf.exempt
def gestao_vista_api_criar_indicador():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Indicador criado com sucesso!',
            'indicador_id': 123
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/gestao-vista/api/meta/atualizar/<int:meta_id>', methods=['PUT'])
@login_required
@csrf.exempt
def gestao_vista_api_atualizar_meta(meta_id):
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': f'Meta {meta_id} atualizada com sucesso!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500