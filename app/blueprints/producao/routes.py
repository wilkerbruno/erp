from flask import render_template, request, jsonify
from flask_login import login_required
from app.blueprints.producao import bp

@bp.route('/')
@login_required
def index():
    return render_template('producao/index.html')

@bp.route('/ordens-producao')
@login_required
def ordens_producao():
    return render_template('producao/ordens_producao.html')

@bp.route('/nova-ordem')
@login_required
def nova_ordem():
    return render_template('producao/nova_ordem.html')

@bp.route('/ordem/<int:ordem_id>')
@login_required
def ver_ordem(ordem_id):
    ordem = {
        'id': ordem_id,
        'numero': f'OP-{ordem_id:04d}',
        'produto': 'Produto A',
        'quantidade': 100,
        'status': 'Em Produção'
    }
    return render_template('producao/ver_ordem.html', ordem=ordem)

@bp.route('/planejamento')
@login_required
def planejamento():
    return render_template('producao/planejamento.html')

@bp.route('/cronograma')
@login_required
def cronograma():
    return render_template('producao/cronograma.html')

@bp.route('/capacidade')
@login_required
def capacidade():
    return render_template('producao/capacidade.html')

@bp.route('/controle-qualidade')
@login_required
def controle_qualidade():
    return render_template('producao/controle_qualidade.html')

@bp.route('/inspecoes')
@login_required
def inspecoes():
    return render_template('producao/inspecoes.html')

@bp.route('/maquinas')
@login_required
def maquinas():
    return render_template('producao/maquinas.html')

@bp.route('/manutencao')
@login_required
def manutencao():
    return render_template('producao/manutencao.html')

@bp.route('/estoque')
@login_required
def estoque():
    return render_template('producao/estoque.html')

@bp.route('/materiais')
@login_required
def materiais():
    return render_template('producao/materiais.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    return render_template('producao/relatorios.html')

@bp.route('/indicadores')
@login_required
def indicadores():
    return render_template('producao/indicadores.html')

@bp.route('/configuracoes')
@login_required
def configuracoes():
    return render_template('producao/configuracoes.html')

@bp.route('/salvar-ordem', methods=['POST'])
@login_required
def salvar_ordem():
    try:
        dados = request.get_json() if request.is_json else request.form.to_dict()
        return jsonify({
            'success': True,
            'message': 'Ordem criada com sucesso!',
            'ordem_id': 1001
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })
