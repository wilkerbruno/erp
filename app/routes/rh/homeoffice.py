from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app import app, db, csrf
from app.models.colaborador import Colaborador
from app.models.homeoffice import AutorizacaoHomeOffice, AuxilioCelular
from datetime import datetime, date


@app.route('/rh/home-office')
@login_required
def rh_home_office():
    return render_template('rh/home_office.html')


# Autorizacoes Home Office - APIs

@app.route('/rh/api/home-office', methods=['GET'])
@login_required
def rh_api_listar_home_office():
    try:
        status = request.args.get('status', 'todos')
        colaborador_id = request.args.get('colaborador_id', type=int)

        query = AutorizacaoHomeOffice.query

        if status == 'ativo':
            query = query.filter_by(status='ativo')
        elif status == 'expirado':
            query = query.filter_by(status='expirado')
        elif status == 'cancelado':
            query = query.filter_by(status='cancelado')

        if colaborador_id:
            query = query.filter_by(colaborador_id=colaborador_id)

        autorizacoes = query.order_by(AutorizacaoHomeOffice.created_at.desc()).all()

        resultado = []
        for a in autorizacoes:
            dados = a.to_dict()
            colaborador = Colaborador.query.get(a.colaborador_id)
            dados['colaborador_nome'] = colaborador.nome_completo if colaborador else None
            resultado.append(dados)

        return jsonify({
            'status': 'success',
            'autorizacoes': resultado,
            'total': len(resultado)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/home-office', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_criar_home_office():
    try:
        data = request.get_json()

        if not data.get('colaborador_id'):
            return jsonify({'status': 'error', 'message': 'colaborador_id obrigatorio'}), 400
        if not data.get('data_inicio'):
            return jsonify({'status': 'error', 'message': 'data_inicio obrigatoria'}), 400

        colaborador = Colaborador.query.get(data['colaborador_id'])
        if not colaborador:
            return jsonify({'status': 'error', 'message': 'Colaborador nao encontrado'}), 404

        ativa_existente = AutorizacaoHomeOffice.query.filter_by(
            colaborador_id=data['colaborador_id'],
            status='ativo'
        ).first()
        if ativa_existente:
            return jsonify({'status': 'error', 'message': 'Colaborador ja possui autorizacao ativa'}), 400

        autorizacao = AutorizacaoHomeOffice(
            colaborador_id=data['colaborador_id'],
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data.get('data_fim') else None,
            dias_semana=data.get('dias_semana'),
            autorizado_por=current_user.id,
            motivo=data.get('motivo'),
            observacoes=data.get('observacoes'),
            status='ativo'
        )

        db.session.add(autorizacao)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Home office autorizado para {colaborador.nome_completo}',
            'autorizacao': autorizacao.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/home-office/<int:autorizacao_id>', methods=['GET'])
@login_required
def rh_api_obter_home_office(autorizacao_id):
    try:
        autorizacao = AutorizacaoHomeOffice.query.get_or_404(autorizacao_id)
        dados = autorizacao.to_dict()
        colaborador = Colaborador.query.get(autorizacao.colaborador_id)
        dados['colaborador_nome'] = colaborador.nome_completo if colaborador else None
        return jsonify({
            'status': 'success',
            'autorizacao': dados
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/home-office/<int:autorizacao_id>', methods=['PUT'])
@login_required
@csrf.exempt
def rh_api_atualizar_home_office(autorizacao_id):
    try:
        autorizacao = AutorizacaoHomeOffice.query.get_or_404(autorizacao_id)
        data = request.get_json()

        if 'data_inicio' in data:
            autorizacao.data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d').date()
        if 'data_fim' in data:
            autorizacao.data_fim = datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data['data_fim'] else None
        if 'dias_semana' in data:
            autorizacao.dias_semana = data['dias_semana']
        if 'motivo' in data:
            autorizacao.motivo = data['motivo']
        if 'observacoes' in data:
            autorizacao.observacoes = data['observacoes']
        if 'status' in data and data['status'] in ['ativo', 'expirado', 'cancelado']:
            autorizacao.status = data['status']

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Autorizacao atualizada',
            'autorizacao': autorizacao.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/home-office/<int:autorizacao_id>/cancelar', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_cancelar_home_office(autorizacao_id):
    try:
        autorizacao = AutorizacaoHomeOffice.query.get_or_404(autorizacao_id)
        if autorizacao.status != 'ativo':
            return jsonify({'status': 'error', 'message': 'Autorizacao nao esta ativa'}), 400

        autorizacao.status = 'cancelado'
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Autorizacao cancelada'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/home-office/verificar/<int:colaborador_id>', methods=['GET'])
@login_required
def rh_api_verificar_home_office(colaborador_id):
    try:
        data_verificar = request.args.get('data')
        if data_verificar:
            data_ref = datetime.strptime(data_verificar, '%Y-%m-%d').date()
        else:
            data_ref = date.today()

        autorizacao = AutorizacaoHomeOffice.query.filter(
            AutorizacaoHomeOffice.colaborador_id == colaborador_id,
            AutorizacaoHomeOffice.data_inicio <= data_ref,
            db.or_(
                AutorizacaoHomeOffice.data_fim >= data_ref,
                AutorizacaoHomeOffice.data_fim.is_(None)
            ),
            AutorizacaoHomeOffice.status == 'ativo'
        ).first()

        autorizado = autorizacao is not None
        dia_permitido = True
        if autorizado and autorizacao.dias_semana:
            dias_map = {0: 'segunda', 1: 'terca', 2: 'quarta', 3: 'quinta', 4: 'sexta', 5: 'sabado', 6: 'domingo'}
            dia_atual = dias_map.get(data_ref.weekday())
            dia_permitido = dia_atual in autorizacao.dias_semana

        return jsonify({
            'status': 'success',
            'autorizado': autorizado and dia_permitido,
            'autorizacao_ativa': autorizado,
            'dia_permitido': dia_permitido,
            'data': data_ref.isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Auxilio Celular - APIs

@app.route('/rh/api/auxilio-celular', methods=['GET'])
@login_required
def rh_api_listar_auxilio_celular():
    try:
        colaborador_id = request.args.get('colaborador_id', type=int)
        query = AuxilioCelular.query.filter_by(ativo=True)

        if colaborador_id:
            query = query.filter_by(colaborador_id=colaborador_id)

        auxilios = query.order_by(AuxilioCelular.created_at.desc()).all()

        resultado = []
        for a in auxilios:
            colaborador = Colaborador.query.get(a.colaborador_id)
            resultado.append({
                'id': a.id,
                'colaborador_id': a.colaborador_id,
                'colaborador_nome': colaborador.nome_completo if colaborador else None,
                'valor_mensal': float(a.valor_mensal),
                'data_inicio': a.data_inicio.isoformat() if a.data_inicio else None,
                'data_fim': a.data_fim.isoformat() if a.data_fim else None,
                'motivo_concessao': a.motivo_concessao,
                'ativo': a.ativo
            })

        return jsonify({
            'status': 'success',
            'auxilios': resultado,
            'total': len(resultado)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/auxilio-celular', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_criar_auxilio_celular():
    try:
        data = request.get_json()

        if not data.get('colaborador_id'):
            return jsonify({'status': 'error', 'message': 'colaborador_id obrigatorio'}), 400
        if not data.get('valor_mensal'):
            return jsonify({'status': 'error', 'message': 'valor_mensal obrigatorio'}), 400

        colaborador = Colaborador.query.get(data['colaborador_id'])
        if not colaborador:
            return jsonify({'status': 'error', 'message': 'Colaborador nao encontrado'}), 404

        existente = AuxilioCelular.query.filter_by(
            colaborador_id=data['colaborador_id'],
            ativo=True
        ).first()
        if existente:
            return jsonify({'status': 'error', 'message': 'Colaborador ja possui auxilio celular ativo'}), 400

        auxilio = AuxilioCelular(
            colaborador_id=data['colaborador_id'],
            valor_mensal=data['valor_mensal'],
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date() if data.get('data_inicio') else date.today(),
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data.get('data_fim') else None,
            motivo_concessao=data.get('motivo_concessao'),
            criado_por=current_user.id,
            ativo=True
        )

        db.session.add(auxilio)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Auxilio celular concedido para {colaborador.nome_completo}'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/auxilio-celular/<int:auxilio_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def rh_api_cancelar_auxilio_celular(auxilio_id):
    try:
        auxilio = AuxilioCelular.query.get_or_404(auxilio_id)
        auxilio.ativo = False
        auxilio.data_fim = date.today()
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Auxilio celular cancelado'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
