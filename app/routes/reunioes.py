from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, csrf


@app.route('/reunioes/')
@login_required
def reunioes_index():
    return render_template('reunioes/index.html')


@app.route('/reunioes/agenda')
@login_required
def reunioes_agenda():
    return render_template('reunioes/agenda.html')


@app.route('/reunioes/atas')
@login_required
def reunioes_atas():
    return render_template('reunioes/atas.html')


@app.route('/reunioes/participantes')
@login_required
def reunioes_participantes():
    return render_template('reunioes/participantes.html')


@app.route('/reunioes/acoes')
@login_required
def reunioes_acoes():
    return render_template('reunioes/acoes.html')


@app.route('/reunioes/salas')
@login_required
def reunioes_salas():
    return render_template('reunioes/salas.html')


@app.route('/reunioes/nova-reuniao')
@login_required
def reunioes_nova():
    return render_template('reunioes/nova_reuniao.html')


@app.route('/reunioes/api/reuniao/criar', methods=['POST'])
@login_required
@csrf.exempt
def reunioes_api_criar():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Reuniao agendada com sucesso!',
            'reuniao_id': 123
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/reunioes/api/ata/criar', methods=['POST'])
@login_required
@csrf.exempt
def reunioes_api_criar_ata():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Ata criada com sucesso!',
            'ata_id': 456
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500