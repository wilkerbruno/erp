from flask import render_template, request, jsonify, make_response
from flask_login import login_required, current_user
from app.blueprints.efo import bp
import json
from datetime import datetime

@bp.route('/')
@login_required
def index():
    return render_template('efo/index.html')

@bp.route('/diagnostico')
@login_required
def diagnostico():
    return render_template('efo/diagnostico.html')

@bp.route('/diagnostico/<int:diagnostico_id>')
@login_required
def ver_diagnostico(diagnostico_id):
    return render_template('efo/ver_diagnostico.html', diagnostico_id=diagnostico_id)

@bp.route('/novo-diagnostico')
@login_required
def novo_diagnostico():
    return render_template('efo/novo_diagnostico.html')

@bp.route('/resultados')
@login_required
def resultados():
    return render_template('efo/resultados.html')

@bp.route('/api/salvar-diagnostico', methods=['POST'])
@login_required
def salvar_diagnostico():
    try:
        dados = request.get_json()
        # Aqui seria a lógica para calcular o EFO e salvar
        
        # Cálculo simulado do EFO
        eficiencia = dados.get('eficiencia', 0)
        flexibilidade = dados.get('flexibilidade', 0)
        organizacao = dados.get('organizacao', 0)
        
        efo_score = (eficiencia + flexibilidade + organizacao) / 3
        
        diagnostico_id = 1000 + hash(str(datetime.now())) % 1000
        
        return jsonify({
            'success': True,
            'message': 'Diagnóstico EFO salvo com sucesso!',
            'diagnostico_id': diagnostico_id,
            'efo_score': round(efo_score, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/api/dados-efo')
@login_required
def dados_efo():
    # Dados simulados baseados na estrutura típica de EFO
    dados = {
        'empresas_avaliadas': 15,
        'diagnosticos_concluidos': 45,
        'media_efo': 7.2,
        'areas_criticas': ['Organização', 'Flexibilidade'],
        'evolucao_mensal': [6.8, 7.0, 7.1, 7.2, 7.3, 7.2],
        'distribuicao_scores': {
            'excelente': 12,
            'bom': 25,
            'regular': 8,
            'critico': 0
        }
    }
    return jsonify(dados)
