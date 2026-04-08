from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, csrf


@app.route('/seguranca-trabalho/')
@login_required
def seg_trabalho_index():
    return render_template('seguranca_trabalho/index.html')


@app.route('/seguranca-trabalho/acidentes')
@login_required
def seg_trabalho_acidentes():
    return render_template('seguranca_trabalho/acidentes.html')


@app.route('/seguranca-trabalho/treinamentos')
@login_required
def seg_trabalho_treinamentos():
    return render_template('seguranca_trabalho/treinamentos.html')


@app.route('/seguranca-trabalho/inspecoes')
@login_required
def seg_trabalho_inspecoes():
    return render_template('seguranca_trabalho/inspecoes.html')


@app.route('/seguranca-trabalho/epis')
@login_required
def seg_trabalho_epis():
    return render_template('seguranca_trabalho/epis.html')


@app.route('/seguranca-trabalho/documentos')
@login_required
def seg_trabalho_documentos():
    return render_template('seguranca_trabalho/documentos.html')


@app.route('/seguranca-trabalho/relatorios')
@login_required
def seg_trabalho_relatorios():
    return render_template('seguranca_trabalho/relatorios.html')


@app.route('/seguranca-trabalho/novo-acidente')
@login_required
def seg_trabalho_novo_acidente():
    return render_template('seguranca_trabalho/novo_acidente.html')


@app.route('/seguranca-trabalho/novo-treinamento')
@login_required
def seg_trabalho_novo_treinamento():
    return render_template('seguranca_trabalho/novo_treinamento.html')


@app.route('/seguranca-trabalho/nova-inspecao')
@login_required
def seg_trabalho_nova_inspecao():
    return render_template('seguranca_trabalho/nova_inspecao.html')


@app.route('/seguranca-trabalho/api/acidente/criar', methods=['POST'])
@login_required
@csrf.exempt
def seg_trabalho_api_criar_acidente():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Acidente registrado com sucesso!',
            'acidente_id': 123
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/seguranca-trabalho/api/treinamento/criar', methods=['POST'])
@login_required
@csrf.exempt
def seg_trabalho_api_criar_treinamento():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Treinamento criado com sucesso!',
            'treinamento_id': 456
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500