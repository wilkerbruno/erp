from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.blueprints.financeiro import bp

@bp.route('/')
@login_required
def index():
    """Dashboard principal do financeiro"""
    return render_template('financeiro/index.html')

@bp.route('/dre-gerencial')
@login_required
def dre_gerencial():
    """DRE Gerencial - Demonstração do Resultado do Exercício"""
    return render_template('financeiro/dre_gerencial.html')

@bp.route('/contas-pagar')
@login_required
def contas_pagar():
    """Gestão de Contas a Pagar"""
    return render_template('financeiro/contas_pagar.html')

@bp.route('/contas-receber')
@login_required
def contas_receber():
    """Gestão de Contas a Receber"""
    return render_template('financeiro/contas_receber.html')

@bp.route('/nova-transacao')
@login_required
def nova_transacao():
    """Nova Transação Financeira"""
    return render_template('financeiro/nova_transacao.html')

@bp.route('/fluxo-caixa')
@login_required
def fluxo_caixa():
    """Controle de Fluxo de Caixa"""
    return render_template('financeiro/fluxo_caixa.html')

@bp.route('/conciliacao-bancaria')
@login_required
def conciliacao_bancaria():
    """Conciliação Bancária"""
    return render_template('financeiro/conciliacao_bancaria.html')

@bp.route('/relatorios-financeiros')
@login_required
def relatorios_financeiros():
    """Relatórios Financeiros"""
    return render_template('financeiro/relatorios_financeiros.html')

@bp.route('/centros-custo')
@login_required
def centros_custo():
    """Gestão de Centros de Custo"""
    return render_template('financeiro/centros_custo.html')

@bp.route('/plano-contas')
@login_required
def plano_contas():
    """Plano de Contas"""
    return render_template('financeiro/plano_contas.html')

@bp.route('/orcamentos')
@login_required
def orcamentos():
    """Controle de Orçamentos"""
    return render_template('financeiro/orcamentos.html')

@bp.route('/tesouraria')
@login_required
def tesouraria():
    """Controle de Tesouraria"""
    return render_template('financeiro/tesouraria.html')

# APIs para ações AJAX
@bp.route('/api/titulo/receber/<int:titulo_id>', methods=['POST'])
@login_required
def api_receber_titulo(titulo_id):
    """API para receber título"""
    try:
        # Aqui seria a lógica para receber o título
        return jsonify({
            'success': True,
            'message': 'Título {} recebido com sucesso!'.format(titulo_id)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao receber título: {}'.format(str(e))
        }), 500

@bp.route('/api/titulo/pagar/<int:titulo_id>', methods=['POST'])
@login_required
def api_pagar_titulo(titulo_id):
    """API para pagar título"""
    try:
        # Aqui seria a lógica para pagar o título
        return jsonify({
            'success': True,
            'message': 'Título {} pago com sucesso!'.format(titulo_id)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao pagar título: {}'.format(str(e))
        }), 500

@bp.route('/api/transacao/criar', methods=['POST'])
@login_required
def api_criar_transacao():
    """API para criar nova transação"""
    try:
        data = request.get_json()
        # Aqui seria a lógica para criar a transação
        redirect_url = url_for('financeiro.contas_receber') if data.get('tipo') in ['receber', 'recebimento'] else url_for('financeiro.contas_pagar')
        return jsonify({
            'success': True,
            'message': 'Transação criada com sucesso!',
            'redirect': redirect_url
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao criar transação: {}'.format(str(e))
        }), 500

@bp.route('/configuracoes')
@login_required
def configuracoes():
    """Configurações Financeiras"""
    return render_template('financeiro/configuracoes_financeiro.html')