from flask import render_template, jsonify, request
from flask_login import login_required
from app.blueprints.financeiro import bp

@bp.route('/')
@login_required
def index():
    '''Dashboard financeiro principal'''
    return render_template('financeiro/index.html')

@bp.route('/dre')
@login_required
def dre():
    '''DRE - Demonstrativo de Resultado do Exercicio'''
    return render_template('financeiro/dre.html')

@bp.route('/fluxo-caixa')
@login_required
def fluxo_caixa():
    '''Fluxo de Caixa'''
    return render_template('financeiro/index.html')

@bp.route('/contas-receber')
@login_required
def contas_receber():
    '''Contas a Receber'''
    return render_template('financeiro/index.html')

@bp.route('/contas-pagar')
@login_required
def contas_pagar():
    '''Contas a Pagar'''
    return render_template('financeiro/index.html')

@bp.route('/api/dados-financeiros')
@login_required
def api_dados_financeiros():
    '''API para dados dos graficos'''
    periodo = request.args.get('periodo', 'mensal')
    
    # Dados simulados - em producao viria do banco
    dados = {
        'dre': {
            'meses': ['Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
            'receitas': [2300000, 2450000, 2280000, 2690000, 2540000, 2847650],
            'despesas': [1850000, 1920000, 1780000, 2100000, 1960000, 1923420],
            'lucros': [450000, 530000, 500000, 590000, 580000, 924230]
        },
        'despesas_categoria': {
            'labels': ['Pessoal', 'Materia Prima', 'Operacionais', 'Marketing', 'Administrativo', 'Outros'],
            'valores': [35, 28, 15, 8, 10, 4]
        },
        'fluxo_caixa': {
            'meses': ['Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'valores': [2134560, 2250000, 2380000, 2190000, 2450000, 2690000, 2580000, 2720000, 2850000, 2680000, 2780000, 2920000]
        }
    }
    
    return jsonify(dados)

@bp.route('/api/kpis')
@login_required
def api_kpis():
    '''API para KPIs financeiros'''
    kpis = {
        'faturamento_mes': 2847650,
        'faturamento_variacao': 12.3,
        'despesas_mes': 1923420,
        'despesas_variacao': -2.1,
        'lucro_liquido': 924230,
        'lucro_variacao': 18.7,
        'margem_lucro': 32.5,
        'margem_variacao': 2.1,
        'contas_receber': 1456780,
        'contas_pagar': 789340,
        'fluxo_caixa': 2134560
    }
    
    return jsonify(kpis)

@bp.route('/relatorio/<tipo>')
@login_required
def relatorio(tipo):
    '''Gera relatorios especificos'''
    if tipo == 'dre':
        return render_template('financeiro/dre.html')
    elif tipo == 'fluxo':
        return render_template('financeiro/index.html')
    else:
        return render_template('financeiro/index.html')
