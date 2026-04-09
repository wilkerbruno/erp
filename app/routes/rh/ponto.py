from flask import request, jsonify, render_template
from flask_login import login_required
from app import app, db, csrf
from app.models.colaborador import Colaborador
from app.models.ponto import RegistroPonto
from app.models.homeoffice import AutorizacaoHomeOffice
from datetime import datetime, date, time as time_type
from math import radians, sin, cos, sqrt, atan2


@app.route('/rh/bater-ponto')
@login_required
def rh_bater_ponto():
    return render_template('rh/ponto/bater_ponto.html')


@app.route('/rh/gerenciar-ponto')
@login_required
def rh_gerenciar_ponto():
    return render_template('rh/ponto/gerenciar_ponto.html')


@app.route('/rh/controle-ponto')
@login_required
def rh_controle_ponto():
    return render_template('rh/ponto/controle_ponto.html')


@app.route('/rh/api/registrar-ponto', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_registrar_ponto():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Dados JSON obrigatorios'}), 400

        colaborador_id = data.get('colaborador_id')
        if not colaborador_id:
            return jsonify({'status': 'error', 'message': 'colaborador_id obrigatorio'}), 400

        colaborador = Colaborador.query.get(colaborador_id)
        if not colaborador:
            return jsonify({'status': 'error', 'message': 'Colaborador nao encontrado'}), 404

        tipo = data.get('tipo')
        tipos_validos = ['entrada', 'saida_almoco', 'volta_almoco', 'saida']
        if tipo not in tipos_validos:
            return jsonify({'status': 'error', 'message': f'Tipo invalido. Use: {tipos_validos}'}), 400

        data_ponto = date.today()
        if data.get('data'):
            try:
                data_ponto = datetime.strptime(data['data'], '%Y-%m-%d').date()
            except ValueError:
                pass

        horario_str = data.get('horario')
        if horario_str:
            try:
                partes = horario_str.split(':')
                horario_ponto = time_type(int(partes[0]), int(partes[1]), int(partes[2]) if len(partes) > 2 else 0)
            except (ValueError, IndexError):
                horario_ponto = datetime.now().time()
        else:
            horario_ponto = datetime.now().time()

        duplicado = RegistroPonto.query.filter_by(
            colaborador_id=colaborador_id,
            data=data_ponto,
            tipo=tipo
        ).first()
        if duplicado:
            return jsonify({'status': 'error', 'message': f'Ponto de {tipo} ja registrado hoje'}), 400

        atraso_minutos = 0
        dentro_horario = True
        if tipo == 'entrada' and colaborador.horario_entrada:
            horario_esperado = colaborador.horario_entrada
            if horario_ponto > horario_esperado:
                diff = datetime.combine(data_ponto, horario_ponto) - datetime.combine(data_ponto, horario_esperado)
                atraso_minutos = int(diff.total_seconds() / 60)
                dentro_horario = False

        home_office = data.get('home_office', False)
        home_office_autorizado = False
        if home_office:
            autorizacao = AutorizacaoHomeOffice.query.filter(
                AutorizacaoHomeOffice.colaborador_id == colaborador_id,
                AutorizacaoHomeOffice.data_inicio <= data_ponto,
                db.or_(
                    AutorizacaoHomeOffice.data_fim >= data_ponto,
                    AutorizacaoHomeOffice.data_fim.is_(None)
                ),
                AutorizacaoHomeOffice.status == 'ativo'
            ).first()
            home_office_autorizado = autorizacao is not None

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        distancia = None
        if latitude and longitude:
            lat_empresa = -19.9674
            lon_empresa = -44.1983
            R = 6371000
            lat1, lat2 = radians(float(latitude)), radians(lat_empresa)
            dlat = radians(lat_empresa - float(latitude))
            dlon = radians(lon_empresa - float(longitude))
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            distancia = R * 2 * atan2(sqrt(a), sqrt(1 - a))

        registro = RegistroPonto(
            colaborador_id=colaborador_id,
            data=data_ponto,
            horario=horario_ponto,
            tipo=tipo,
            latitude=latitude,
            longitude=longitude,
            localizacao_texto=data.get('localizacao_texto', ''),
            distancia_empresa=round(distancia, 2) if distancia else None,
            home_office=home_office,
            home_office_autorizado=home_office_autorizado,
            dentro_horario=dentro_horario,
            atraso_minutos=atraso_minutos,
            dispositivo=data.get('dispositivo', ''),
            ip_address=request.remote_addr
        )

        db.session.add(registro)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Ponto registrado com sucesso',
            'registro': registro.to_dict(),
            'atraso_minutos': atraso_minutos,
            'dentro_horario': dentro_horario,
            'home_office_autorizado': home_office_autorizado,
            'distancia_empresa': round(distancia, 2) if distancia else None
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/ponto/hoje/<int:colaborador_id>', methods=['GET'])
@login_required
def rh_api_ponto_hoje(colaborador_id):
    try:
        registros = RegistroPonto.query.filter_by(
            colaborador_id=colaborador_id,
            data=date.today()
        ).order_by(RegistroPonto.horario.asc()).all()

        return jsonify({
            'status': 'success',
            'registros': [r.to_dict() for r in registros],
            'total': len(registros)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/ponto/periodo/<int:colaborador_id>', methods=['GET'])
@login_required
def rh_api_ponto_periodo(colaborador_id):
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')

        if not data_inicio or not data_fim:
            primeiro_dia = date.today().replace(day=1)
            data_inicio_dt = primeiro_dia
            data_fim_dt = date.today()
        else:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d').date()

        registros = RegistroPonto.query.filter(
            RegistroPonto.colaborador_id == colaborador_id,
            RegistroPonto.data >= data_inicio_dt,
            RegistroPonto.data <= data_fim_dt
        ).order_by(RegistroPonto.data.asc(), RegistroPonto.horario.asc()).all()

        dias = {}
        for r in registros:
            dia_str = r.data.isoformat()
            if dia_str not in dias:
                dias[dia_str] = {
                    'data': dia_str,
                    'registros': [],
                    'total_atrasos': 0
                }
            dias[dia_str]['registros'].append(r.to_dict())
            dias[dia_str]['total_atrasos'] += r.atraso_minutos or 0

        return jsonify({
            'status': 'success',
            'dias': list(dias.values()),
            'total_dias': len(dias),
            'periodo': {
                'inicio': data_inicio_dt.isoformat(),
                'fim': data_fim_dt.isoformat()
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/ponto/resumo-mensal', methods=['GET'])
@login_required
def rh_api_ponto_resumo_mensal():
    try:
        mes = request.args.get('mes', date.today().month, type=int)
        ano = request.args.get('ano', date.today().year, type=int)

        primeiro_dia = date(ano, mes, 1)
        if mes == 12:
            ultimo_dia = date(ano + 1, 1, 1)
        else:
            ultimo_dia = date(ano, mes + 1, 1)

        colaboradores = Colaborador.query.filter_by(ativo=True).order_by(Colaborador.nome_completo).all()
        resumo = []

        for colab in colaboradores:
            registros = RegistroPonto.query.filter(
                RegistroPonto.colaborador_id == colab.id,
                RegistroPonto.data >= primeiro_dia,
                RegistroPonto.data < ultimo_dia
            ).all()

            dias_trabalhados = len(set(r.data for r in registros))
            total_atrasos = sum(r.atraso_minutos or 0 for r in registros if r.tipo == 'entrada')
            total_home_office = len(set(r.data for r in registros if r.home_office))

            resumo.append({
                'colaborador_id': colab.id,
                'nome': colab.nome_completo,
                'departamento': colab.departamento.nome if colab.departamento_id else None,
                'dias_trabalhados': dias_trabalhados,
                'total_atrasos_minutos': total_atrasos,
                'dias_home_office': total_home_office,
                'total_registros': len(registros)
            })

        return jsonify({
            'status': 'success',
            'resumo': resumo,
            'mes': mes,
            'ano': ano
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/ponto/<int:registro_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def rh_api_excluir_ponto(registro_id):
    try:
        registro = RegistroPonto.query.get_or_404(registro_id)
        db.session.delete(registro)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Registro de ponto excluido'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500