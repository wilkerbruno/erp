from flask import render_template, request, jsonify
from flask_login import login_required
from app import app, db, csrf
from app.models.colaborador import Colaborador
from app.models.cargo import Cargo
from app.models.departamento import Departamento
from datetime import datetime, date
from sqlalchemy import func


@app.route('/rh/')
@login_required
def rh_index():
    return render_template('rh/index.html')


@app.route('/rh/colaboradores')
@login_required
def rh_colaboradores():
    return render_template('rh/colaboradores.html')


@app.route('/rh/novo-colaborador')
@login_required
def rh_novo_colaborador():
    return render_template('rh/novo_colaborador.html')


@app.route('/rh/colaborador/<int:colaborador_id>')
@login_required
def rh_ver_colaborador(colaborador_id):
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    return render_template('rh/ver_colaborador.html', colaborador=colaborador)


@app.route('/rh/colaborador/editar/<int:colaborador_id>')
@login_required
def rh_editar_colaborador(colaborador_id):
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    return render_template('rh/editar_colaborador.html', colaborador=colaborador)


@app.route('/rh/relatorio-frequencias')
@login_required
def rh_relatorio_frequencias():
    return render_template('rh/relatorio_frequencias.html')


@app.route('/rh/gerenciar-ferias')
@login_required
def rh_gerenciar_ferias():
    return render_template('rh/gerenciar_ferias.html')


@app.route('/rh/exportar-dados')
@login_required
def rh_exportar_dados():
    return render_template('rh/exportar_dados.html')


@app.route('/rh/relatorios')
@login_required
def rh_relatorios():
    return render_template('rh/relatorios.html')


# APIs

@app.route('/rh/api/colaboradores', methods=['GET'])
@login_required
def rh_api_listar_colaboradores():
    try:
        status = request.args.get('status', 'todos')
        departamento_id = request.args.get('departamento_id', '', type=str)
        busca = request.args.get('busca', '')

        query = Colaborador.query

        if status == 'ativos':
            query = query.filter(Colaborador.ativo == True)
        elif status == 'inativos':
            query = query.filter(Colaborador.ativo == False)

        if departamento_id:
            query = query.filter(Colaborador.departamento_id == int(departamento_id))

        if busca:
            termo = f'%{busca}%'
            query = query.filter(
                db.or_(
                    Colaborador.nome_completo.ilike(termo),
                    Colaborador.cpf.ilike(termo),
                    Colaborador.email.ilike(termo),
                    Colaborador.matricula.ilike(termo)
                )
            )

        query = query.order_by(Colaborador.nome_completo.asc())
        colaboradores = query.all()

        return jsonify({
            'status': 'success',
            'colaboradores': [c.to_dict() for c in colaboradores],
            'total': len(colaboradores)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores/estatisticas', methods=['GET'])
@login_required
def rh_api_estatisticas():
    try:
        total = Colaborador.query.count()
        ativos = Colaborador.query.filter_by(ativo=True).count()

        primeiro_dia_mes = date.today().replace(day=1)
        novos_mes = Colaborador.query.filter(
            Colaborador.data_admissao >= primeiro_dia_mes
        ).count()

        departamentos = db.session.query(
            func.count(func.distinct(Colaborador.departamento_id))
        ).scalar()

        return jsonify({
            'status': 'success',
            'total': total,
            'ativos': ativos,
            'novos_mes': novos_mes,
            'departamentos': departamentos or 0
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores', methods=['POST'])
@login_required
@csrf.exempt
def rh_api_criar_colaborador():
    try:
        data = request.get_json()

        if not data.get('nome_completo'):
            return jsonify({'status': 'error', 'message': 'Nome e obrigatorio'}), 400
        if not data.get('cpf'):
            return jsonify({'status': 'error', 'message': 'CPF e obrigatorio'}), 400
        if not data.get('data_admissao'):
            return jsonify({'status': 'error', 'message': 'Data de admissao e obrigatoria'}), 400

        existente = Colaborador.query.filter_by(cpf=data['cpf']).first()
        if existente:
            return jsonify({'status': 'error', 'message': 'CPF ja cadastrado'}), 400

        matricula = data.get('matricula')
        if not matricula:
            ultimo = Colaborador.query.order_by(Colaborador.id.desc()).first()
            proximo_id = (ultimo.id + 1) if ultimo else 1
            matricula = f'COL{proximo_id:05d}'

        colaborador = Colaborador(
            nome_completo=data['nome_completo'],
            cpf=data['cpf'],
            rg=data.get('rg'),
            data_nascimento=datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date() if data.get('data_nascimento') else None,
            sexo=data.get('sexo'),
            estado_civil=data.get('estado_civil'),
            email=data.get('email'),
            telefone=data.get('telefone'),
            celular=data.get('celular'),
            endereco=data.get('endereco'),
            numero=data.get('numero'),
            complemento=data.get('complemento'),
            bairro=data.get('bairro'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            cep=data.get('cep'),
            cargo_id=data.get('cargo_id', type=int) if data.get('cargo_id') else None,
            departamento_id=data.get('departamento_id', type=int) if data.get('departamento_id') else None,
            matricula=matricula,
            data_admissao=datetime.strptime(data['data_admissao'], '%Y-%m-%d').date(),
            tipo_contrato=data.get('tipo_contrato', 'CLT'),
            jornada_trabalho=data.get('jornada_trabalho', '44h semanais'),
            salario_base=data.get('salario_base'),
            banco=data.get('banco'),
            agencia=data.get('agencia'),
            conta=data.get('conta'),
            tipo_conta=data.get('tipo_conta'),
            pix=data.get('pix'),
            observacoes=data.get('observacoes'),
            ativo=True
        )

        db.session.add(colaborador)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Colaborador cadastrado com sucesso',
            'colaborador': colaborador.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores/<int:colaborador_id>', methods=['GET'])
@login_required
def rh_api_obter_colaborador(colaborador_id):
    try:
        colaborador = Colaborador.query.get_or_404(colaborador_id)
        return jsonify({
            'status': 'success',
            'colaborador': colaborador.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores/<int:colaborador_id>', methods=['PUT'])
@login_required
@csrf.exempt
def rh_api_atualizar_colaborador(colaborador_id):
    try:
        colaborador = Colaborador.query.get_or_404(colaborador_id)
        data = request.get_json()

        campos_texto = [
            'nome_completo', 'cpf', 'rg', 'sexo', 'estado_civil',
            'email', 'telefone', 'celular',
            'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep',
            'tipo_contrato', 'jornada_trabalho', 'matricula',
            'banco', 'agencia', 'conta', 'tipo_conta', 'pix',
            'observacoes'
        ]

        for campo in campos_texto:
            if campo in data:
                setattr(colaborador, campo, data[campo])

        if 'cargo_id' in data:
            colaborador.cargo_id = int(data['cargo_id']) if data['cargo_id'] else None
        if 'departamento_id' in data:
            colaborador.departamento_id = int(data['departamento_id']) if data['departamento_id'] else None
        if 'salario_base' in data:
            colaborador.salario_base = data['salario_base']
        if 'ativo' in data:
            colaborador.ativo = data['ativo']

        if 'data_nascimento' in data and data['data_nascimento']:
            colaborador.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        if 'data_admissao' in data and data['data_admissao']:
            colaborador.data_admissao = datetime.strptime(data['data_admissao'], '%Y-%m-%d').date()
        if 'data_demissao' in data and data['data_demissao']:
            colaborador.data_demissao = datetime.strptime(data['data_demissao'], '%Y-%m-%d').date()

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Colaborador atualizado com sucesso',
            'colaborador': colaborador.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/colaboradores/<int:colaborador_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def rh_api_desativar_colaborador(colaborador_id):
    try:
        colaborador = Colaborador.query.get_or_404(colaborador_id)
        data = request.get_json() or {}

        colaborador.ativo = False
        colaborador.data_demissao = date.today()
        colaborador.observacoes = data.get('motivo', 'Desligamento')

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Colaborador {colaborador.nome_completo} desativado'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/cargos', methods=['GET'])
@login_required
def rh_api_listar_cargos():
    try:
        cargos = Cargo.query.filter_by(ativo=True).order_by(Cargo.nome).all()
        return jsonify({
            'status': 'success',
            'cargos': [c.to_dict() for c in cargos]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/rh/api/departamentos', methods=['GET'])
@login_required
def rh_api_listar_departamentos():
    try:
        departamentos = Departamento.query.filter_by(ativo=True).order_by(Departamento.nome).all()
        return jsonify({
            'status': 'success',
            'departamentos': [d.to_dict() for d in departamentos]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Beneficios - Paginas

@app.route('/rh/beneficios')
@login_required
def rh_beneficios():
    return render_template('rh/beneficios.html')


# Beneficios - APIs

@app.route('/rh/api/beneficios', methods=['GET'])
@login_required
def rh_api_listar_beneficios():
    try:
        from app.models.beneficio import Beneficio
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
        from app.models.beneficio import Beneficio
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
        from app.models.beneficio import Beneficio
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
        from app.models.beneficio import Beneficio
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
        from app.models.beneficio import Beneficio
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
        from app.models.beneficio import ColaboradorBeneficio, Beneficio
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
        from app.models.beneficio import ColaboradorBeneficio, Beneficio
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
        from app.models.beneficio import ColaboradorBeneficio
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
