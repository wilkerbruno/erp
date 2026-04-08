from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, csrf


@app.route('/producao/')
@login_required
def producao_index():
    return render_template('producao/index.html')


@app.route('/producao/ordens-producao')
@login_required
def producao_ordens():
    return render_template('producao/ordens_producao.html')


@app.route('/producao/nova-ordem')
@login_required
def producao_nova_ordem():
    return render_template('producao/nova_ordem.html')


@app.route('/producao/ordem/<int:ordem_id>')
@login_required
def producao_ver_ordem(ordem_id):
    ordem = {
        'id': ordem_id,
        'numero': f'OP-{ordem_id:04d}',
        'produto': 'Produto A',
        'quantidade': 100,
        'status': 'Em Producao'
    }
    return render_template('producao/ver_ordem.html', ordem=ordem)


@app.route('/producao/planejamento')
@login_required
def producao_planejamento():
    return render_template('producao/planejamento.html')


@app.route('/producao/cronograma')
@login_required
def producao_cronograma():
    return render_template('producao/cronograma.html')


@app.route('/producao/capacidade')
@login_required
def producao_capacidade():
    return render_template('producao/capacidade.html')


@app.route('/producao/controle-qualidade')
@login_required
def producao_controle_qualidade():
    return render_template('producao/controle_qualidade.html')


@app.route('/producao/inspecoes')
@login_required
def producao_inspecoes():
    return render_template('producao/inspecoes.html')


@app.route('/producao/maquinas')
@login_required
def producao_maquinas():
    return render_template('producao/maquinas.html')


@app.route('/producao/manutencao')
@login_required
def producao_manutencao():
    return render_template('producao/manutencao.html')


@app.route('/producao/estoque')
@login_required
def producao_estoque():
    return render_template('producao/estoque.html')


@app.route('/producao/materiais')
@login_required
def producao_materiais():
    return render_template('producao/materiais.html')


@app.route('/producao/relatorios')
@login_required
def producao_relatorios():
    return render_template('producao/relatorios.html')


@app.route('/producao/indicadores')
@login_required
def producao_indicadores():
    return render_template('producao/indicadores.html')


@app.route('/producao/configuracoes')
@login_required
def producao_configuracoes():
    return render_template('producao/configuracoes.html')


@app.route('/producao/salvar-ordem', methods=['POST'])
@login_required
@csrf.exempt
def producao_salvar_ordem():
    try:
        dados = request.get_json() if request.is_json else request.form.to_dict()
        return jsonify({
            'success': True,
            'message': 'Ordem criada com sucesso!',
            'ordem_id': 1001
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
