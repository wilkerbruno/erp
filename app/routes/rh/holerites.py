from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app import app, db, csrf
from app.models.colaborador import Colaborador
from app.models.holerite import Holerite
from app.models.beneficio import ColaboradorBeneficio, Beneficio
from datetime import datetime, date
from decimal import Decimal


TABELA_INSS_2025 = [
    (1518.00, Decimal('0.075')),
    (2793.88, Decimal('0.09')),
    (4190.83, Decimal('0.12')),
    (8157.41, Decimal('0.14')),
]

TABELA_IRRF_2025 = [
    (2259.20, Decimal('0'), Decimal('0')),
    (2826.65, Decimal('0.075'), Decimal('169.44')),
    (3751.05, Decimal('0.15'), Decimal('381.44')),
    (4664.68, Decimal('0.225'), Decimal('662.77')),
    (Decimal('999999999'), Decimal('0.275'), Decimal('896.00')),
]

DEDUCAO_DEPENDENTE = Decimal('189.59')


def calcular_inss(salario_bruto):
    bruto = Decimal(str(salario_bruto))
    inss = Decimal('0')
    faixa_anterior = Decimal('0')
    for teto, aliquota in TABELA_INSS_2025:
        teto_d = Decimal(str(teto))
        if bruto <= teto_d:
            inss += (bruto - faixa_anterior) * aliquota
            break
        else:
            inss += (teto_d - faixa_anterior) * aliquota
            faixa_anterior = teto_d
    teto_inss = Decimal('951.63')
    return min(inss, teto_inss).quantize(Decimal('0.01'))


def calcular_irrf(base_irrf, num_dependentes=0):
    base = Decimal(str(base_irrf)) - (DEDUCAO_DEPENDENTE * num_dependentes)
    if base <= 0:
        return Decimal('0')
    for teto, aliquota, deducao in TABELA_IRRF_2025:
        teto_d = Decimal(str(teto))
        if base <= teto_d:
            irrf = base * aliquota - Decimal(str(deducao))
            return max(irrf, Decimal('0')).quantize(Decimal('0.01'))
    return Decimal('0')


@app.route('/rh/holerites')
@login_required
def rh_holerites():
    return render_template('rh/holerites.html')


@app.route('/rh/api/holerites', methods=['GET'])
@login_required
def rh_api_listar_holerites():
    try:
        mes = request.args.get('mes', type=int)
        ano = request.args.get('ano', type=int)
        colaborador_id = request.args.get('colaborador_id', type=int)
        status = request.args.get('status')

        query = Holerite.query

        if mes:
            query = query.filter_by(mes=mes)
        if ano:
            query = query.filter_by(ano=ano)
        if colaborador_id:
            query = query.filter_by(colaborador_id=colaborador_id)
        if status:
            query = query.filter_by(status=status)

        holerites = query.order_by(Holerite.ano.desc(), Holerite.mes.desc()).all()

        resultado = []
        for h in holerites:
            dados = h.to_dict()
            colaborador = Colaborador.query.get(h.colaborador_id)
            dados['colaborador_nome'] = colaborador.nome_completo if colaborador else None
            resultado.append(dados)

        return jsonify({
            'status': 'success',
            'holerites': resultado,
            'total': len(resultado)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/holerites/<int:holerite_id>', methods=['GET'])
@login_required
def rh_api_obter_holerite(holerite_id):
    try:
        holerite = Holerite.query.get_or_404(holerite_id)
        dados = holerite.to_dict()
        colaborador = Colaborador.query.get(holerite.colaborador_id)
        dados['colaborador_nome'] = colaborador.nome_completo if colaborador else None
        dados['detalhes'] = {
            'horas_extras': float(holerite.horas_extras),
            'adicional_noturno': float(holerite.adicional_noturno),
            'comissoes': float(holerite.comissoes),
            'bonus': float(holerite.bonus),
            'vale_alimentacao': float(holerite.vale_alimentacao),
            'vale_transporte': float(holerite.vale_transporte),
            'auxilio_celular': float(holerite.auxilio_celular),
            'plano_saude': float(holerite.plano_saude),
            'outros_beneficios': float(holerite.outros_beneficios),
            'inss': float(holerite.inss),
            'irrf': float(holerite.irrf),
            'vale_transporte_desconto': float(holerite.vale_transporte_desconto),
            'plano_saude_desconto': float(holerite.plano_saude_desconto),
            'faltas': float(holerite.faltas),
            'atrasos': float(holerite.atrasos),
            'adiantamento': float(holerite.adiantamento),
            'emprestimos': float(holerite.emprestimos),
            'outros_descontos': float(holerite.outros_descontos),
            'base_inss': float(holerite.base_inss),
            'base_irrf': float(holerite.base_irrf),
            'base_fgts': float(holerite.base_fgts),
            'fgts': float(holerite.fgts)
        }
        return jsonify({
            'status': 'success',
            'holerite': dados
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/holerites/gerar', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_gerar_holerite():
    try:
        data = request.get_json()

        if not data.get('colaborador_id'):
            return jsonify({'status': 'error', 'message': 'colaborador_id obrigatorio'}), 400
        if not data.get('mes') or not data.get('ano'):
            return jsonify({'status': 'error', 'message': 'mes e ano obrigatorios'}), 400

        colaborador = Colaborador.query.get(data['colaborador_id'])
        if not colaborador:
            return jsonify({'status': 'error', 'message': 'Colaborador nao encontrado'}), 404

        existente = Holerite.query.filter_by(
            colaborador_id=data['colaborador_id'],
            mes=data['mes'],
            ano=data['ano']
        ).first()
        if existente:
            return jsonify({'status': 'error', 'message': f'Holerite ja existe para {data["mes"]}/{data["ano"]}'}), 400

        salario_base = Decimal(str(colaborador.salario_base or 0))
        horas_extras = Decimal(str(data.get('horas_extras', 0)))
        adicional_noturno = Decimal(str(data.get('adicional_noturno', 0)))
        comissoes = Decimal(str(data.get('comissoes', 0)))
        bonus = Decimal(str(data.get('bonus', 0)))

        vale_alimentacao = Decimal('0')
        vale_transporte = Decimal('0')
        auxilio_celular = Decimal('0')
        plano_saude = Decimal('0')
        outros_beneficios = Decimal('0')

        vinculos = ColaboradorBeneficio.query.filter_by(
            colaborador_id=colaborador.id,
            ativo=True
        ).all()
        for v in vinculos:
            beneficio = Beneficio.query.get(v.beneficio_id)
            if not beneficio:
                continue
            valor = Decimal(str(v.valor_customizado)) if v.valor_customizado else Decimal(str(beneficio.valor_fixo or 0))
            nome_lower = beneficio.nome.lower()
            if 'alimenta' in nome_lower or 'refeic' in nome_lower:
                vale_alimentacao += valor
            elif 'transporte' in nome_lower:
                vale_transporte += valor
            elif 'celular' in nome_lower:
                auxilio_celular += valor
            elif 'saude' in nome_lower or 'medic' in nome_lower:
                plano_saude += valor
            else:
                outros_beneficios += valor

        total_vencimentos = (salario_base + horas_extras + adicional_noturno +
                             comissoes + bonus + vale_alimentacao + vale_transporte +
                             auxilio_celular + plano_saude + outros_beneficios)

        base_inss = salario_base + horas_extras + adicional_noturno + comissoes + bonus
        inss = calcular_inss(base_inss)

        base_irrf = base_inss - inss
        irrf = calcular_irrf(base_irrf)

        vt_desconto = Decimal(str(data.get('vale_transporte_desconto', 0)))
        ps_desconto = Decimal(str(data.get('plano_saude_desconto', 0)))
        faltas_desc = Decimal(str(data.get('faltas', 0)))
        atrasos_desc = Decimal(str(data.get('atrasos', 0)))
        adiantamento = Decimal(str(data.get('adiantamento', 0)))
        emprestimos = Decimal(str(data.get('emprestimos', 0)))
        outros_descontos = Decimal(str(data.get('outros_descontos', 0)))

        total_descontos = (inss + irrf + vt_desconto + ps_desconto +
                           faltas_desc + atrasos_desc + adiantamento +
                           emprestimos + outros_descontos)

        liquido = total_vencimentos - total_descontos

        base_fgts = base_inss
        fgts = (base_fgts * Decimal('0.08')).quantize(Decimal('0.01'))

        holerite = Holerite(
            colaborador_id=colaborador.id,
            mes=data['mes'],
            ano=data['ano'],
            salario_base=salario_base,
            horas_extras=horas_extras,
            adicional_noturno=adicional_noturno,
            comissoes=comissoes,
            bonus=bonus,
            vale_alimentacao=vale_alimentacao,
            vale_transporte=vale_transporte,
            auxilio_celular=auxilio_celular,
            plano_saude=plano_saude,
            outros_beneficios=outros_beneficios,
            total_vencimentos=total_vencimentos,
            inss=inss,
            irrf=irrf,
            vale_transporte_desconto=vt_desconto,
            plano_saude_desconto=ps_desconto,
            faltas=faltas_desc,
            atrasos=atrasos_desc,
            adiantamento=adiantamento,
            emprestimos=emprestimos,
            outros_descontos=outros_descontos,
            total_descontos=total_descontos,
            liquido=liquido,
            base_inss=base_inss,
            base_irrf=base_irrf,
            base_fgts=base_fgts,
            fgts=fgts,
            observacoes=data.get('observacoes'),
            status='gerado',
            gerado_por=current_user.id
        )

        db.session.add(holerite)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Holerite gerado para {colaborador.nome_completo} - {data["mes"]}/{data["ano"]}',
            'holerite': holerite.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/holerites/gerar-lote', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_gerar_holerites_lote():
    try:
        data = request.get_json()
        mes = data.get('mes')
        ano = data.get('ano')

        if not mes or not ano:
            return jsonify({'status': 'error', 'message': 'mes e ano obrigatorios'}), 400

        colaboradores = Colaborador.query.filter_by(ativo=True).all()
        gerados = 0
        erros = []

        for colab in colaboradores:
            existente = Holerite.query.filter_by(
                colaborador_id=colab.id, mes=mes, ano=ano
            ).first()
            if existente:
                erros.append(f'{colab.nome_completo}: ja existe')
                continue

            if not colab.salario_base or colab.salario_base <= 0:
                erros.append(f'{colab.nome_completo}: sem salario base')
                continue

            salario_base = Decimal(str(colab.salario_base))

            vale_alimentacao = Decimal('0')
            vale_transporte = Decimal('0')
            auxilio_celular_val = Decimal('0')
            plano_saude = Decimal('0')
            outros_beneficios = Decimal('0')

            vinculos = ColaboradorBeneficio.query.filter_by(
                colaborador_id=colab.id, ativo=True
            ).all()
            for v in vinculos:
                beneficio = Beneficio.query.get(v.beneficio_id)
                if not beneficio:
                    continue
                valor = Decimal(str(v.valor_customizado)) if v.valor_customizado else Decimal(str(beneficio.valor_fixo or 0))
                nome_lower = beneficio.nome.lower()
                if 'alimenta' in nome_lower or 'refeic' in nome_lower:
                    vale_alimentacao += valor
                elif 'transporte' in nome_lower:
                    vale_transporte += valor
                elif 'celular' in nome_lower:
                    auxilio_celular_val += valor
                elif 'saude' in nome_lower or 'medic' in nome_lower:
                    plano_saude += valor
                else:
                    outros_beneficios += valor

            total_vencimentos = (salario_base + vale_alimentacao + vale_transporte +
                                 auxilio_celular_val + plano_saude + outros_beneficios)

            inss = calcular_inss(salario_base)
            base_irrf = salario_base - inss
            irrf = calcular_irrf(base_irrf)
            total_descontos = inss + irrf
            liquido = total_vencimentos - total_descontos
            fgts = (salario_base * Decimal('0.08')).quantize(Decimal('0.01'))

            holerite = Holerite(
                colaborador_id=colab.id,
                mes=mes, ano=ano,
                salario_base=salario_base,
                vale_alimentacao=vale_alimentacao,
                vale_transporte=vale_transporte,
                auxilio_celular=auxilio_celular_val,
                plano_saude=plano_saude,
                outros_beneficios=outros_beneficios,
                total_vencimentos=total_vencimentos,
                inss=inss, irrf=irrf,
                total_descontos=total_descontos,
                liquido=liquido,
                base_inss=salario_base,
                base_irrf=base_irrf,
                base_fgts=salario_base,
                fgts=fgts,
                status='gerado',
                gerado_por=current_user.id
            )
            db.session.add(holerite)
            gerados += 1

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'{gerados} holerites gerados para {mes}/{ano}',
            'gerados': gerados,
            'erros': erros
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/holerites/<int:holerite_id>', methods=['PUT'])
@login_required
@csrf.exempt
def rh_api_atualizar_holerite(holerite_id):
    try:
        holerite = Holerite.query.get_or_404(holerite_id)
        data = request.get_json()

        if 'status' in data and data['status'] in ['gerado', 'enviado', 'pago']:
            holerite.status = data['status']
        if 'data_pagamento' in data and data['data_pagamento']:
            holerite.data_pagamento = datetime.strptime(data['data_pagamento'], '%Y-%m-%d').date()
        if 'observacoes' in data:
            holerite.observacoes = data['observacoes']

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Holerite atualizado',
            'holerite': holerite.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/holerites/<int:holerite_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def rh_api_excluir_holerite(holerite_id):
    try:
        holerite = Holerite.query.get_or_404(holerite_id)
        if holerite.status == 'pago':
            return jsonify({'status': 'error', 'message': 'Nao e possivel excluir holerite ja pago'}), 400
        db.session.delete(holerite)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Holerite excluido'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
