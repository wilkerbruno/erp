from flask import request, jsonify, render_template
from flask_login import login_required
from app import app, db, csrf
from app.models.colaborador import Colaborador
from app.models.beneficio import Beneficio, ColaboradorBeneficio, CargoBeneficio
from datetime import datetime, date


@app.route('/rh/beneficios')
@login_required
def rh_beneficios():
    return render_template('rh/beneficios.html')


@app.route('/rh/api/beneficios', methods=['GET'])
@login_required
def rh_api_listar_beneficios():
    try:
        status = request.args.get('status', 'todos')
        query = Beneficio.query
        if status == 'ativos':
            query = query.filter_by(ativo=True)
        elif status == 'inativos':
            query = query.filter_by(ativo=False)
        beneficios = query.order_by(Beneficio.nome).all()
        return jsonify({
            'status': 'success',
            'beneficios': [b.to_dict() for b in beneficios],
            'total': len(beneficios)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/beneficios', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_criar_beneficio():
    try:
        data = request.get_json()
        if not data.get('nome'):
            return jsonify({'status': 'error', 'message': 'Nome e obrigatorio'}), 400

        beneficio = Beneficio(
            nome=data['nome'],
            descricao=data.get('descricao'),
            tipo=data.get('tipo', 'fixo'),
            valor_fixo=data.get('valor_fixo'),
            percentual=data.get('percentual'),
            requer_desempenho=data.get('requer_desempenho', False),
            meta_minima=data.get('meta_minima'),
            ativo=True
        )
        db.session.add(beneficio)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Beneficio criado com sucesso',
            'beneficio': beneficio.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/beneficios/<int:beneficio_id>', methods=['GET'])
@login_required
def rh_api_obter_beneficio(beneficio_id):
    try:
        beneficio = Beneficio.query.get_or_404(beneficio_id)
        return jsonify({
            'status': 'success',
            'beneficio': beneficio.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/beneficios/<int:beneficio_id>', methods=['PUT'])
@login_required
@csrf.exempt
def rh_api_atualizar_beneficio(beneficio_id):
    try:
        beneficio = Beneficio.query.get_or_404(beneficio_id)
        data = request.get_json()

        if 'nome' in data:
            beneficio.nome = data['nome']
        if 'descricao' in data:
            beneficio.descricao = data['descricao']
        if 'tipo' in data:
            beneficio.tipo = data['tipo']
        if 'valor_fixo' in data:
            beneficio.valor_fixo = data['valor_fixo']
        if 'percentual' in data:
            beneficio.percentual = data['percentual']
        if 'requer_desempenho' in data:
            beneficio.requer_desempenho = data['requer_desempenho']
        if 'meta_minima' in data:
            beneficio.meta_minima = data['meta_minima']
        if 'ativo' in data:
            beneficio.ativo = data['ativo']

        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Beneficio atualizado',
            'beneficio': beneficio.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/beneficios/<int:beneficio_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def rh_api_excluir_beneficio(beneficio_id):
    try:
        beneficio = Beneficio.query.get_or_404(beneficio_id)
        beneficio.ativo = False
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Beneficio {beneficio.nome} desativado'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores/<int:colaborador_id>/beneficios', methods=['GET'])
@login_required
def rh_api_beneficios_colaborador(colaborador_id):
    try:
        colaborador = Colaborador.query.get_or_404(colaborador_id)
        vinculos = ColaboradorBeneficio.query.filter_by(
            colaborador_id=colaborador_id,
            ativo=True
        ).all()
        resultado = []
        for v in vinculos:
            beneficio = Beneficio.query.get(v.beneficio_id)
            if beneficio:
                resultado.append({
                    'vinculo_id': v.id,
                    'beneficio_id': v.beneficio_id,
                    'nome': beneficio.nome,
                    'tipo': beneficio.tipo,
                    'valor': float(v.valor_customizado) if v.valor_customizado else float(beneficio.valor_fixo) if beneficio.valor_fixo else None,
                    'data_inicio': v.data_inicio.isoformat() if v.data_inicio else None,
                    'data_fim': v.data_fim.isoformat() if v.data_fim else None
                })
        return jsonify({
            'status': 'success',
            'beneficios': resultado,
            'colaborador': colaborador.nome_completo
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores/<int:colaborador_id>/beneficios', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_vincular_beneficio(colaborador_id):
    try:
        Colaborador.query.get_or_404(colaborador_id)
        data = request.get_json()

        if not data.get('beneficio_id'):
            return jsonify({'status': 'error', 'message': 'beneficio_id e obrigatorio'}), 400

        Beneficio.query.get_or_404(data['beneficio_id'])

        existente = ColaboradorBeneficio.query.filter_by(
            colaborador_id=colaborador_id,
            beneficio_id=data['beneficio_id'],
            ativo=True
        ).first()
        if existente:
            return jsonify({'status': 'error', 'message': 'Beneficio ja vinculado'}), 400

        vinculo = ColaboradorBeneficio(
            colaborador_id=colaborador_id,
            beneficio_id=data['beneficio_id'],
            valor_customizado=data.get('valor_customizado'),
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date() if data.get('data_inicio') else date.today(),
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data.get('data_fim') else None,
            ativo=True
        )
        db.session.add(vinculo)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Beneficio vinculado ao colaborador'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores/<int:colaborador_id>/beneficios/<int:vinculo_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def rh_api_desvincular_beneficio(colaborador_id, vinculo_id):
    try:
        vinculo = ColaboradorBeneficio.query.filter_by(
            id=vinculo_id,
            colaborador_id=colaborador_id
        ).first_or_404()
        vinculo.ativo = False
        vinculo.data_fim = date.today()
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Beneficio desvinculado'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500