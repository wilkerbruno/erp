from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, csrf


@app.route('/financeiro/')
@login_required
def financeiro_index():
    return render_template('financeiro/index.html')


@app.route('/financeiro/dre-gerencial')
@login_required
def financeiro_dre_gerencial():
    return render_template('financeiro/dre_gerencial.html')


@app.route('/financeiro/contas-pagar')
@login_required
def financeiro_contas_pagar():
    return render_template('financeiro/contas_pagar.html')


@app.route('/financeiro/contas-receber')
@login_required
def financeiro_contas_receber():
    return render_template('financeiro/contas_receber.html')


@app.route('/financeiro/nova-transacao')
@login_required
def financeiro_nova_transacao():
    return render_template('financeiro/nova_transacao.html')


@app.route('/financeiro/fluxo-caixa')
@login_required
def financeiro_fluxo_caixa():
    return render_template('financeiro/fluxo_caixa.html')


@app.route('/financeiro/conciliacao-bancaria')
@login_required
def financeiro_conciliacao_bancaria():
    return render_template('financeiro/conciliacao_bancaria.html')


@app.route('/financeiro/relatorios-financeiros')
@login_required
def financeiro_relatorios_financeiros():
    return render_template('financeiro/relatorios_financeiros.html')


@app.route('/financeiro/centros-custo')
@login_required
def financeiro_centros_custo():
    return render_template('financeiro/centros_custo.html')


@app.route('/financeiro/plano-contas')
@login_required
def financeiro_plano_contas():
    return render_template('financeiro/plano_contas.html')


@app.route('/financeiro/orcamentos')
@login_required
def financeiro_orcamentos():
    return render_template('financeiro/orcamentos.html')


@app.route('/financeiro/tesouraria')
@login_required
def financeiro_tesouraria():
    return render_template('financeiro/tesouraria.html')


@app.route('/financeiro/configuracoes')
@login_required
def financeiro_configuracoes():
    return render_template('financeiro/configuracoes_financeiro.html')


@app.route('/financeiro/api/titulo/receber/<int:titulo_id>', methods=['POST'])
@login_required
@csrf.exempt
def financeiro_api_receber_titulo(titulo_id):
    try:
        return jsonify({
            'success': True,
            'message': f'Titulo {titulo_id} recebido com sucesso!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/financeiro/api/titulo/pagar/<int:titulo_id>', methods=['POST'])
@login_required
@csrf.exempt
def financeiro_api_pagar_titulo(titulo_id):
    try:
        return jsonify({
            'success': True,
            'message': f'Titulo {titulo_id} pago com sucesso!'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/financeiro/api/transacao/criar', methods=['POST'])
@login_required
@csrf.exempt
def financeiro_api_criar_transacao():
    try:
        data = request.get_json()
        tipo = data.get('tipo', '')
        redirect_url = '/financeiro/contas-receber' if tipo in ['receber', 'recebimento'] else '/financeiro/contas-pagar'
        return jsonify({
            'success': True,
            'message': 'Transacao criada com sucesso!',
            'redirect': redirect_url
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
