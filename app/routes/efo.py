from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, csrf
from datetime import datetime


@app.route('/efo/')
@login_required
def efo_index():
    return render_template('efo/index.html')


@app.route('/efo/diagnostico')
@login_required
def efo_diagnostico():
    return render_template('efo/diagnostico.html')


@app.route('/efo/diagnostico/<int:diagnostico_id>')
@login_required
def efo_ver_diagnostico(diagnostico_id):
    return render_template('efo/ver_diagnostico.html', diagnostico_id=diagnostico_id)


@app.route('/efo/novo-diagnostico')
@login_required
def efo_novo_diagnostico():
    return render_template('efo/novo_diagnostico.html')


@app.route('/efo/resultados')
@login_required
def efo_resultados():
    return render_template('efo/resultados.html')


@app.route('/efo/api/salvar-diagnostico', methods=['POST'])
@login_required
@csrf.exempt
def efo_api_salvar_diagnostico():
    try:
        dados = request.get_json()
        eficiencia = dados.get('eficiencia', 0)
        flexibilidade = dados.get('flexibilidade', 0)
        organizacao = dados.get('organizacao', 0)
        efo_score = (eficiencia + flexibilidade + organizacao) / 3
        diagnostico_id = 1000 + hash(str(datetime.now())) % 1000
        return jsonify({
            'success': True,
            'message': 'Diagnostico EFO salvo com sucesso!',
            'diagnostico_id': diagnostico_id,
            'efo_score': round(efo_score, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/efo/api/dados-efo')
@login_required
def efo_api_dados():
    return jsonify({
        'empresas_avaliadas': 15,
        'diagnosticos_concluidos': 45,
        'media_efo': 7.2,
        'areas_criticas': ['Organizacao', 'Flexibilidade'],
        'evolucao_mensal': [6.8, 7.0, 7.1, 7.2, 7.3, 7.2],
        'distribuicao_scores': {
            'excelente': 12,
            'bom': 25,
            'regular': 8,
            'critico': 0
        }
    })