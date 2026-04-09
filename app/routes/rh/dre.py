from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app import app, db, csrf
from app.models.dre import DREGerencial
from datetime import datetime
from decimal import Decimal


@app.route('/rh/dre')
@login_required
def rh_dre():
    return render_template('rh/dre.html')


@app.route('/rh/api/dre', methods=['GET'])
@login_required
def rh_api_listar_dre():
    try:
        ano = request.args.get('ano', type=int)
        query = DREGerencial.query

        if ano:
            query = query.filter_by(ano=ano)

        registros = query.order_by(DREGerencial.ano.desc(), DREGerencial.mes.desc()).all()

        return jsonify({
            'status': 'success',
            'registros': [r.to_dict() for r in registros],
            'total': len(registros)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/dre/<int:dre_id>', methods=['GET'])
@login_required
def rh_api_obter_dre(dre_id):
    try:
        dre = DREGerencial.query.get_or_404(dre_id)
        dados = dre.to_dict()
        dados['detalhes'] = {
            'receita_bruta': float(dre.receita_bruta),
            'deducoes': float(dre.deducoes),
            'receita_liquida': float(dre.receita_liquida),
            'custo_mercadorias': float(dre.custo_mercadorias),
            'custo_servicos': float(dre.custo_servicos),
            'lucro_bruto': float(dre.lucro_bruto),
            'despesas_vendas': float(dre.despesas_vendas),
            'comissoes_vendas': float(dre.comissoes_vendas),
            'despesas_administrativas': float(dre.despesas_administrativas),
            'salarios_encargos': float(dre.salarios_encargos),
            'aluguel': float(dre.aluguel),
            'despesas_financeiras': float(dre.despesas_financeiras),
            'receitas_financeiras': float(dre.receitas_financeiras),
            'resultado_operacional': float(dre.resultado_operacional),
            'impostos_contribuicoes': float(dre.impostos_contribuicoes),
            'resultado_liquido': float(dre.resultado_liquido),
            'margem_bruta': float(dre.margem_bruta) if dre.margem_bruta else None,
            'margem_operacional': float(dre.margem_operacional) if dre.margem_operacional else None,
            'margem_liquida': float(dre.margem_liquida) if dre.margem_liquida else None,
            'importado_de': dre.importado_de,
            'arquivo_origem': dre.arquivo_origem,
            'observacoes': dre.observacoes
        }
        return jsonify({
            'status': 'success',
            'dre': dados
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/dre', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_criar_dre():
    try:
        data = request.get_json()

        if not data.get('mes') or not data.get('ano'):
            return jsonify({'status': 'error', 'message': 'mes e ano obrigatorios'}), 400

        existente = DREGerencial.query.filter_by(
            mes=data['mes'], ano=data['ano']
        ).first()
        if existente:
            return jsonify({'status': 'error', 'message': f'DRE ja existe para {data["mes"]}/{data["ano"]}'}), 400

        receita_bruta = Decimal(str(data.get('receita_bruta', 0)))
        deducoes = Decimal(str(data.get('deducoes', 0)))
        receita_liquida = receita_bruta - deducoes

        custo_mercadorias = Decimal(str(data.get('custo_mercadorias', 0)))
        custo_servicos = Decimal(str(data.get('custo_servicos', 0)))
        lucro_bruto = receita_liquida - custo_mercadorias - custo_servicos

        despesas_vendas = Decimal(str(data.get('despesas_vendas', 0)))
        comissoes_vendas = Decimal(str(data.get('comissoes_vendas', 0)))
        despesas_administrativas = Decimal(str(data.get('despesas_administrativas', 0)))
        salarios_encargos = Decimal(str(data.get('salarios_encargos', 0)))
        aluguel = Decimal(str(data.get('aluguel', 0)))
        despesas_financeiras = Decimal(str(data.get('despesas_financeiras', 0)))
        receitas_financeiras = Decimal(str(data.get('receitas_financeiras', 0)))

        total_despesas_op = (despesas_vendas + comissoes_vendas + despesas_administrativas +
                             salarios_encargos + aluguel)
        resultado_operacional = lucro_bruto - total_despesas_op - despesas_financeiras + receitas_financeiras

        impostos_contribuicoes = Decimal(str(data.get('impostos_contribuicoes', 0)))
        resultado_liquido = resultado_operacional - impostos_contribuicoes

        margem_bruta = None
        margem_operacional = None
        margem_liquida = None
        if receita_liquida > 0:
            margem_bruta = (lucro_bruto / receita_liquida * 100).quantize(Decimal('0.01'))
            margem_operacional = (resultado_operacional / receita_liquida * 100).quantize(Decimal('0.01'))
            margem_liquida = (resultado_liquido / receita_liquida * 100).quantize(Decimal('0.01'))

        dre = DREGerencial(
            mes=data['mes'],
            ano=data['ano'],
            receita_bruta=receita_bruta,
            deducoes=deducoes,
            receita_liquida=receita_liquida,
            custo_mercadorias=custo_mercadorias,
            custo_servicos=custo_servicos,
            lucro_bruto=lucro_bruto,
            despesas_vendas=despesas_vendas,
            comissoes_vendas=comissoes_vendas,
            despesas_administrativas=despesas_administrativas,
            salarios_encargos=salarios_encargos,
            aluguel=aluguel,
            despesas_financeiras=despesas_financeiras,
            receitas_financeiras=receitas_financeiras,
            resultado_operacional=resultado_operacional,
            impostos_contribuicoes=impostos_contribuicoes,
            resultado_liquido=resultado_liquido,
            margem_bruta=margem_bruta,
            margem_operacional=margem_operacional,
            margem_liquida=margem_liquida,
            observacoes=data.get('observacoes'),
            importado_de=data.get('importado_de', 'manual'),
            criado_por=current_user.id
        )

        db.session.add(dre)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'DRE criada para {data["mes"]}/{data["ano"]}',
            'dre': dre.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/dre/<int:dre_id>', methods=['PUT'])
@login_required
@csrf.exempt
def rh_api_atualizar_dre(dre_id):
    try:
        dre = DREGerencial.query.get_or_404(dre_id)
        data = request.get_json()

        campos_decimal = [
            'receita_bruta', 'deducoes', 'custo_mercadorias', 'custo_servicos',
            'despesas_vendas', 'comissoes_vendas', 'despesas_administrativas',
            'salarios_encargos', 'aluguel', 'despesas_financeiras',
            'receitas_financeiras', 'impostos_contribuicoes'
        ]

        for campo in campos_decimal:
            if campo in data:
                setattr(dre, campo, Decimal(str(data[campo])))

        if 'observacoes' in data:
            dre.observacoes = data['observacoes']

        dre.receita_liquida = dre.receita_bruta - dre.deducoes
        dre.lucro_bruto = dre.receita_liquida - dre.custo_mercadorias - dre.custo_servicos

        total_despesas_op = (dre.despesas_vendas + dre.comissoes_vendas +
                             dre.despesas_administrativas + dre.salarios_encargos + dre.aluguel)
        dre.resultado_operacional = (dre.lucro_bruto - total_despesas_op -
                                     dre.despesas_financeiras + dre.receitas_financeiras)
        dre.resultado_liquido = dre.resultado_operacional - dre.impostos_contribuicoes

        if dre.receita_liquida > 0:
            rl = dre.receita_liquida
            dre.margem_bruta = (dre.lucro_bruto / rl * 100).quantize(Decimal('0.01'))
            dre.margem_operacional = (dre.resultado_operacional / rl * 100).quantize(Decimal('0.01'))
            dre.margem_liquida = (dre.resultado_liquido / rl * 100).quantize(Decimal('0.01'))

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'DRE atualizada',
            'dre': dre.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/dre/<int:dre_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def rh_api_excluir_dre(dre_id):
    try:
        dre = DREGerencial.query.get_or_404(dre_id)
        db.session.delete(dre)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'DRE {dre.mes}/{dre.ano} excluida'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/dre/evolucao', methods=['GET'])
@login_required
def rh_api_dre_evolucao():
    try:
        ano = request.args.get('ano', type=int)
        meses_atras = request.args.get('meses', 12, type=int)

        if ano:
            registros = DREGerencial.query.filter_by(ano=ano).order_by(DREGerencial.mes.asc()).all()
        else:
            registros = DREGerencial.query.order_by(
                DREGerencial.ano.desc(), DREGerencial.mes.desc()
            ).limit(meses_atras).all()
            registros.reverse()

        evolucao = []
        for r in registros:
            evolucao.append({
                'periodo': f'{r.mes:02d}/{r.ano}',
                'receita_liquida': float(r.receita_liquida),
                'lucro_bruto': float(r.lucro_bruto),
                'resultado_operacional': float(r.resultado_operacional),
                'resultado_liquido': float(r.resultado_liquido),
                'margem_bruta': float(r.margem_bruta) if r.margem_bruta else None,
                'margem_liquida': float(r.margem_liquida) if r.margem_liquida else None
            })

        return jsonify({
            'status': 'success',
            'evolucao': evolucao,
            'total_periodos': len(evolucao)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
