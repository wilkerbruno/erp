from flask import render_template, request, jsonify
from flask_login import UserMixin, login_required
from app.blueprints.rh import bp
from datetime import datetime
from io import BytesIO
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, send_file
from app.models.registros_ponto import RegistroPonto, AutorizacaoHomeOffice
from app.models.user import User
from app import db
from sqlalchemy import and_, func


from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.blueprints.rh import bp
from datetime import datetime, date
import traceback
import json


@bp.route('/')
@login_required
def index():
    """Página principal do RH usando template"""
    return render_template('rh/index.html')

@bp.route('/colaboradores')
@login_required
def colaboradores():
    """Lista de colaboradores usando template"""
    return render_template('rh/colaboradores.html')

@bp.route('/novo-colaborador')
@login_required
def novo_colaborador():
    """Novo colaborador usando template"""
    return render_template('rh/novo_colaborador.html')


# === OUTRAS PÁGINAS BÁSICAS ===

@bp.route('/relatorio-frequencias')
@login_required
def relatorio_frequencias():
    """Relatório de frequências"""
    return render_template('rh/relatorio_frequencias.html')

@bp.route('/gerenciar-ferias')
@login_required
def gerenciar_ferias():
    """Gerenciar férias"""
    return render_template('rh/gerenciar_ferias.html')

@bp.route('/exportar-dados')
@login_required
def exportar_dados():
    """Exportar dados"""
    return render_template('rh/exportar_dados.html')

@bp.route('/relatorios')
@login_required
def relatorios():
    """Página de relatórios"""
    return render_template('rh/relatorios.html')

@bp.route('/colaborador/<int:colaborador_id>')
@login_required
def ver_colaborador(colaborador_id):
    from app.models import Colaborador
    
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    
    return render_template('rh/ver_colaborador.html', colaborador={
        'id': colaborador.id,
        'nome': colaborador.nome_completo,
        'cargo': colaborador.cargo.nome if colaborador.cargo else 'N/A',
        'departamento': colaborador.departamento.nome if colaborador.departamento else 'N/A',
        'email': colaborador.email,
        'telefone': colaborador.telefone,
        'data_admissao': colaborador.data_admissao,
        'salario_base': colaborador.salario_base
    })

@bp.route('/registrar-ponto-acao', methods=['POST'])
@login_required
def registrar_ponto_acao():
    """API para registrar ponto"""
    try:
        dados = request.get_json() if request.is_json else request.form.to_dict()
        tipo = dados.get('tipo', 'entrada')
        horario = dados.get('horario', datetime.now().strftime('%H:%M:%S'))
        
        return jsonify({
            'success': True,
            'message': f'Ponto de {tipo} registrado!',
            'horario': horario,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro: {str(e)}'
        })


# ========== BENEFÍCIOS ==========
@bp.route('/beneficios')
@login_required
def beneficios():
    """Página principal de benefícios"""
    return render_template('rh/beneficios/index.html')

@bp.route('/beneficios/novo', methods=['GET', 'POST'])
@login_required
def novo_beneficio():
    if request.method == 'POST':
        from app.models import Beneficio
        from app import db
        
        data = request.get_json() if request.is_json else request.form
        
        beneficio = Beneficio(
            nome=data.get('nome'),
            tipo=data.get('tipo', 'fixo'),
            valor=data.get('valor'),
            percentual=data.get('percentual'),
            descricao=data.get('descricao'),
            requer_desempenho=data.get('requer_desempenho', False),
            ativo=True
        )
        
        db.session.add(beneficio)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Benefício criado com sucesso!',
            'beneficio_id': beneficio.id
        })
    
    return render_template('rh/beneficios/novo.html')

@bp.route('/api/beneficios')
@login_required
def api_listar_beneficios():
    from app.models import Beneficio
    
    beneficios = Beneficio.query.filter_by(ativo=True).all()
    
    return jsonify({
        'status': 'success',
        'beneficios': [
            {
                'id': b.id,
                'nome': b.nome,
                'tipo': b.tipo,
                'valor': float(b.valor) if b.valor else 0,
                'percentual': float(b.percentual) if b.percentual else 0,
                'descricao': b.descricao,
                'requer_desempenho': b.requer_desempenho,
                'ativo': b.ativo
            }
            for b in beneficios
        ]
    })

@bp.route('/bater-ponto')
@login_required
def bater_ponto():
    """Página para bater ponto com GPS"""
    return render_template('rh/ponto/bater_ponto.html')

@bp.route('/gerenciar-ponto')
@login_required
def gerenciar_ponto():
    """Gerenciar registros de ponto"""
    return render_template('rh/ponto/gerenciar_ponto.html')

@bp.route('/controle-ponto')
@login_required
def controle_ponto():
    """Controle geral de ponto"""
    return render_template('rh/ponto/controle_ponto.html')

@bp.route('/api/registrar-ponto', methods=['POST'])
@login_required
def api_registrar_ponto():
    from app.models import RegistroPonto, AutorizacaoHomeOffice
    from app import db
    from datetime import datetime, date, time
    from sqlalchemy import and_, or_
    
    data = request.get_json()
    
    try:
        # Validar se é home office autorizado
        home_office = data.get('home_office', False)
        home_office_autorizado = False
        
        if home_office:
            hoje = date.today()
            dia_semana = hoje.strftime('%A').lower()  # 'monday', 'tuesday', etc.
            
            # Mapear dias da semana
            dias_map = {
                'monday': 'segunda', 'tuesday': 'terça', 'wednesday': 'quarta',
                'thursday': 'quinta', 'friday': 'sexta', 'saturday': 'sábado', 'sunday': 'domingo'
            }
            dia_pt = dias_map.get(dia_semana)
            
            autorizacao = AutorizacaoHomeOffice.query.filter(
                and_(
                    AutorizacaoHomeOffice.colaborador_id == data['colaborador_id'],
                    AutorizacaoHomeOffice.status == 'ativo',
                    AutorizacaoHomeOffice.data_inicio <= hoje,
                    or_(
                        AutorizacaoHomeOffice.data_fim >= hoje,
                        AutorizacaoHomeOffice.data_fim.is_(None)
                    )
                )
            ).first()
            
            if autorizacao and dia_pt in (autorizacao.dias_semana or []):
                home_office_autorizado = True
        
        # Calcular atraso (exemplo: horário de entrada é 8:00)
        horario_entrada_padrao = time(8, 0)  # 8:00 AM
        horario_atual = datetime.strptime(data['horario'], '%H:%M:%S').time()
        atraso_minutos = 0
        
        if data['tipo'] == 'entrada' and horario_atual > horario_entrada_padrao:
            delta = datetime.combine(date.today(), horario_atual) - datetime.combine(date.today(), horario_entrada_padrao)
            atraso_minutos = int(delta.total_seconds() / 60)
        
        # Criar registro
        registro = RegistroPonto(
            colaborador_id=data['colaborador_id'],
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            tipo=data['tipo'],
            horario=horario_atual,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            localizacao_texto=data.get('localizacao_texto'),
            distancia_empresa=data.get('distancia_empresa'),
            home_office=home_office,
            home_office_autorizado=home_office_autorizado,
            dentro_horario=(atraso_minutos == 0),
            atraso_minutos=atraso_minutos,
            dispositivo=data.get('dispositivo'),
            ip_address=request.remote_addr,
            observacoes=data.get('observacoes')
        )
        
        db.session.add(registro)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Ponto registrado com sucesso!',
            'registro': {
                'id': registro.id,
                'tipo': registro.tipo,
                'horario': registro.horario.strftime('%H:%M:%S'),
                'localizacao': registro.localizacao_texto
            },
            'atraso_minutos': atraso_minutos,
            'home_office_autorizado': home_office_autorizado
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/api/ponto/hoje/<int:colaborador_id>')
@login_required
def api_ponto_hoje(colaborador_id):
    """API: Obter registros de hoje - COM DEBUG DETALHADO"""
    try:
        print("\n" + "="*70)
        print(f"🔍 API PONTO HOJE - Colaborador {colaborador_id}")
        print("="*70)
        
        hoje = date.today()
        print(f"📅 Data de hoje: {hoje}")
        print(f"📅 Tipo da data: {type(hoje)}")
        
        # ✅ CONSULTAR DO BANCO
        try:
            print(f"\n🔍 Consultando banco de dados...")
            
            # Buscar registros
            registros_db = RegistroPonto.query.filter(
                and_(
                    RegistroPonto.colaborador_id == colaborador_id,
                    RegistroPonto.data == hoje
                )
            ).order_by(RegistroPonto.horario.asc()).all()
            
            print(f"✅ Query executada com sucesso!")
            print(f"📊 Registros encontrados: {len(registros_db)}")
            
            # Log de cada registro
            if len(registros_db) > 0:
                print("\n📋 Registros:")
                for idx, r in enumerate(registros_db, 1):
                    print(f"   {idx}. ID: {r.id}")
                    print(f"      Colaborador: {r.colaborador_id}")
                    print(f"      Data: {r.data}")
                    print(f"      Horário: {r.horario}")
                    print(f"      Tipo: {r.tipo}")
                    print(f"      Atraso: {r.atraso_minutos} min")
                    print(f"      Home Office: {r.home_office}")
            else:
                print("⚠️  Nenhum registro encontrado!")
                print("\n🔍 Verificando se há registros no banco...")
                
                # Buscar TODOS os registros do colaborador
                todos_registros = RegistroPonto.query.filter(
                    RegistroPonto.colaborador_id == colaborador_id
                ).all()
                
                print(f"   Total de registros do colaborador: {len(todos_registros)}")
                
                if len(todos_registros) > 0:
                    print("   Datas existentes:")
                    for r in todos_registros:
                        print(f"      - {r.data} ({type(r.data)})")
            
            # Converter para dicionários
            print(f"\n🔄 Convertendo para JSON...")
            registros = []
            
            for r in registros_db:
                try:
                    registro_dict = r.to_dict()
                    registros.append(registro_dict)
                    print(f"   ✅ Registro {r.id} convertido")
                except Exception as e_dict:
                    print(f"   ❌ Erro ao converter registro {r.id}: {e_dict}")
            
            print(f"✅ Total convertido: {len(registros)} registro(s)")
            
        except Exception as e_db:
            print(f"❌ Erro ao consultar banco:")
            print(f"   {e_db}")
            traceback.print_exc()
            registros = []
        
        # Construir resposta
        response_data = {
            'status': 'success',
            'registros': registros,
            'data': str(hoje),
            'colaborador_id': colaborador_id,
            'total': len(registros)
        }
        
        print(f"\n📤 Enviando resposta:")
        print(f"   Status: success")
        print(f"   Total de registros: {len(registros)}")
        print(f"   Data: {hoje}")
        print("="*70 + "\n")
        
        response = jsonify(response_data)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
        
    except Exception as e:
        print(f"\n❌ ERRO GERAL:")
        print(f"   {e}")
        traceback.print_exc()
        print("="*70 + "\n")
        
        response = jsonify({
            'status': 'error',
            'message': str(e),
            'registros': []
        })
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response, 500

# ========== HOME OFFICE ==========
@bp.route('/home-office')
@login_required
def home_office():
    """Página de gerenciamento de home office"""
    return render_template('rh/home_office/home_office.html')

@bp.route('/api/home-office/autorizar', methods=['POST'])
@login_required
def api_autorizar_home_office():
    from app.models import AutorizacaoHomeOffice
    from app import db
    from datetime import datetime
    
    data = request.get_json()
    
    try:
        autorizacao = AutorizacaoHomeOffice(
            colaborador_id=data['colaborador_id'],
            data_inicio=datetime.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            data_fim=datetime.strptime(data['data_fim'], '%Y-%m-%d').date() if data.get('data_fim') else None,
            dias_semana=data.get('dias_semana', []),
            autorizado_por=current_user.id,
            motivo=data.get('motivo'),
            status='ativo'
        )
        
        db.session.add(autorizacao)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Home office autorizado com sucesso!',
            'autorizacao': {
                'id': autorizacao.id,
                'colaborador_id': autorizacao.colaborador_id,
                'data_inicio': autorizacao.data_inicio.isoformat(),
                'data_fim': autorizacao.data_fim.isoformat() if autorizacao.data_fim else None,
                'dias_semana': autorizacao.dias_semana
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/api/home-office/listar')
@login_required
def api_listar_home_office():
    from app.models import AutorizacaoHomeOffice
    
    autorizacoes = AutorizacaoHomeOffice.query.filter_by(status='ativo').all()
    
    return jsonify({
        'status': 'success',
        'autorizacoes': [
            {
                'id': a.id,
                'colaborador_id': a.colaborador_id,
                'colaborador_nome': a.colaborador.nome_completo if a.colaborador else 'N/A',
                'data_inicio': a.data_inicio.isoformat(),
                'data_fim': a.data_fim.isoformat() if a.data_fim else None,
                'dias_semana': a.dias_semana,
                'status': a.status,
                'motivo': a.motivo
            }
            for a in autorizacoes
        ]
    })

# ========== HOLERITES ==========
@bp.route('/holerites')
@login_required
def holerites():
    """Página principal de holerites"""
    return render_template('rh/holerite/holerites.html')

@bp.route('/api/holerite/gerar', methods=['POST'])
@login_required
def api_gerar_holerite():
    from app.models import Holerite, Colaborador, ColaboradorBeneficio
    from app import db
    from decimal import Decimal
    
    data = request.get_json()
    
    try:
        colaborador = Colaborador.query.get_or_404(data['colaborador_id'])
        mes = int(data['mes'])
        ano = int(data['ano'])
        
        # Verificar se já existe holerite para este mês/ano
        holerite_existente = Holerite.query.filter_by(
            colaborador_id=colaborador.id,
            mes=mes,
            ano=ano
        ).first()
        
        if holerite_existente:
            return jsonify({
                'status': 'error',
                'message': f'Já existe holerite para {mes}/{ano}'
            }), 400
        
        # Cálculos
        salario_base = colaborador.salario_base
        
        # Benefícios ativos
        beneficios_ativos = ColaboradorBeneficio.query.filter_by(
            colaborador_id=colaborador.id,
            ativo=True
        ).all()
        
        vale_alimentacao = sum(b.valor_customizado or b.beneficio.valor 
                               for b in beneficios_ativos 
                               if b.beneficio.nome == 'Vale Alimentação')
        
        vale_transporte_valor = sum(b.valor_customizado or b.beneficio.valor 
                                    for b in beneficios_ativos 
                                    if b.beneficio.nome == 'Vale Transporte')
        
        auxilio_celular = sum(b.valor_customizado or b.beneficio.valor 
                              for b in beneficios_ativos 
                              if b.beneficio.nome == 'Auxílio Celular')
        
        # Total de vencimentos
        total_vencimentos = salario_base + vale_alimentacao + vale_transporte_valor + auxilio_celular
        
        # Descontos
        # INSS - Tabela simplificada (2024)
        if salario_base <= Decimal('1412.00'):
            inss = salario_base * Decimal('0.075')
        elif salario_base <= Decimal('2666.68'):
            inss = salario_base * Decimal('0.09')
        elif salario_base <= Decimal('4000.03'):
            inss = salario_base * Decimal('0.12')
        else:
            inss = salario_base * Decimal('0.14')
        
        # IRRF - Tabela simplificada
        base_irrf = salario_base - inss
        if base_irrf <= Decimal('2112.00'):
            irrf = Decimal('0')
        elif base_irrf <= Decimal('2826.65'):
            irrf = (base_irrf * Decimal('0.075')) - Decimal('158.40')
        elif base_irrf <= Decimal('3751.05'):
            irrf = (base_irrf * Decimal('0.15')) - Decimal('370.40')
        elif base_irrf <= Decimal('4664.68'):
            irrf = (base_irrf * Decimal('0.225')) - Decimal('651.73')
        else:
            irrf = (base_irrf * Decimal('0.275')) - Decimal('884.96')
        
        # Vale transporte (desconto 6%)
        vale_transporte_desconto = salario_base * Decimal('0.06') if vale_transporte_valor > 0 else Decimal('0')
        
        total_descontos = inss + irrf + vale_transporte_desconto
        liquido = total_vencimentos - total_descontos
        
        # Criar holerite
        holerite = Holerite(
            colaborador_id=colaborador.id,
            mes=mes,
            ano=ano,
            salario_base=salario_base,
            vale_alimentacao=vale_alimentacao,
            vale_transporte=vale_transporte_valor,
            auxilio_celular=auxilio_celular,
            total_vencimentos=total_vencimentos,
            inss=inss,
            irrf=irrf,
            vale_transporte_desconto=vale_transporte_desconto,
            total_descontos=total_descontos,
            liquido=liquido,
            status='gerado',
            gerado_por=current_user.id
        )
        
        db.session.add(holerite)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Holerite gerado com sucesso!',
            'holerite': {
                'id': holerite.id,
                'colaborador_id': holerite.colaborador_id,
                'colaborador_nome': colaborador.nome_completo,
                'mes': holerite.mes,
                'ano': holerite.ano,
                'salario_base': float(holerite.salario_base),
                'total_vencimentos': float(holerite.total_vencimentos),
                'total_descontos': float(holerite.total_descontos),
                'liquido': float(holerite.liquido)
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/api/holerite/listar')
@login_required
def api_listar_holerites():
    from app.models import Holerite
    
    # Filtros opcionais
    colaborador_id = request.args.get('colaborador_id', type=int)
    mes = request.args.get('mes', type=int)
    ano = request.args.get('ano', type=int)
    
    query = Holerite.query
    
    if colaborador_id:
        query = query.filter_by(colaborador_id=colaborador_id)
    if mes:
        query = query.filter_by(mes=mes)
    if ano:
        query = query.filter_by(ano=ano)
    
    holerites = query.order_by(Holerite.ano.desc(), Holerite.mes.desc()).all()
    
    return jsonify({
        'status': 'success',
        'holerites': [
            {
                'id': h.id,
                'colaborador_id': h.colaborador_id,
                'colaborador_nome': h.colaborador.nome_completo if h.colaborador else 'N/A',
                'mes': h.mes,
                'ano': h.ano,
                'salario_base': float(h.salario_base),
                'total_vencimentos': float(h.total_vencimentos),
                'total_descontos': float(h.total_descontos),
                'liquido': float(h.liquido),
                'status': h.status
            }
            for h in holerites
        ]
    })

@bp.route('/api/holerite/<int:id>/pdf')
@login_required
def api_holerite_pdf(id):
    """API: Gerar PDF do holerite"""
    try:
        # Mock de PDF simples
        buffer = BytesIO()
        buffer.write(b'PDF Mock - Holerite #' + str(id).encode())
        buffer.seek(0)
        
        return send_file(
            buffer, 
            as_attachment=True, 
            download_name=f'holerite_{id}.pdf', 
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# ========== DRE GERENCIAL ==========
@bp.route('/dre')
@login_required
def dre_gerencial():
    """Página de DRE Gerencial"""
    return render_template('rh/dre/dre_gerencial.html')

@bp.route('/api/dre/importar', methods=['POST'])
@login_required
def api_importar_dre():
    from app.models import DREGerencial
    from app import db
    from decimal import Decimal
    
    # Pode vir como form-data (arquivo) ou JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    try:
        mes = int(data.get('mes'))
        ano = int(data.get('ano'))
        
        # Verificar se já existe DRE para este mês/ano
        dre_existente = DREGerencial.query.filter_by(mes=mes, ano=ano).first()
        
        if dre_existente:
            # Atualizar
            dre_existente.receita_bruta = Decimal(data.get('receita_bruta', 0))
            dre_existente.deducoes = Decimal(data.get('deducoes', 0))
            dre_existente.receita_liquida = Decimal(data.get('receita_liquida', 0))
            dre_existente.custo_mercadorias = Decimal(data.get('custo_mercadorias', 0))
            dre_existente.lucro_bruto = Decimal(data.get('lucro_bruto', 0))
            dre_existente.despesas_vendas = Decimal(data.get('despesas_vendas', 0))
            dre_existente.despesas_administrativas = Decimal(data.get('despesas_administrativas', 0))
            dre_existente.despesas_financeiras = Decimal(data.get('despesas_financeiras', 0))
            dre_existente.receitas_financeiras = Decimal(data.get('receitas_financeiras', 0))
            dre_existente.resultado_operacional = Decimal(data.get('resultado_operacional', 0))
            dre_existente.resultado_liquido = Decimal(data.get('resultado_liquido', 0))
            dre_existente.importado_de = data.get('importado_de', 'sistema')
            
            dre = dre_existente
        else:
            # Criar novo
            dre = DREGerencial(
                mes=mes,
                ano=ano,
                receita_bruta=Decimal(data.get('receita_bruta', 0)),
                deducoes=Decimal(data.get('deducoes', 0)),
                receita_liquida=Decimal(data.get('receita_liquida', 0)),
                custo_mercadorias=Decimal(data.get('custo_mercadorias', 0)),
                lucro_bruto=Decimal(data.get('lucro_bruto', 0)),
                despesas_vendas=Decimal(data.get('despesas_vendas', 0)),
                despesas_administrativas=Decimal(data.get('despesas_administrativas', 0)),
                despesas_financeiras=Decimal(data.get('despesas_financeiras', 0)),
                receitas_financeiras=Decimal(data.get('receitas_financeiras', 0)),
                resultado_operacional=Decimal(data.get('resultado_operacional', 0)),
                resultado_liquido=Decimal(data.get('resultado_liquido', 0)),
                importado_de=data.get('importado_de', 'sistema')
            )
            db.session.add(dre)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'DRE importada com sucesso!',
            'dre': {
                'id': dre.id,
                'mes': dre.mes,
                'ano': dre.ano,
                'receita_bruta': float(dre.receita_bruta),
                'resultado_liquido': float(dre.resultado_liquido)
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/api/dre/listar')
@login_required
def api_listar_dre():
    """API: Listar DREs"""
    # Mock de dados
    dres = [
        {
            'id': 1,
            'mes': 1,
            'ano': 2024,
            'receita_bruta': 100000.00,
            'resultado_liquido': 30000.00
        },
        {
            'id': 2,
            'mes': 2,
            'ano': 2024,
            'receita_bruta': 120000.00,
            'resultado_liquido': 35000.00
        }
    ]
    
    return jsonify({
        'status': 'success',
        'dres': dres
    })


@bp.route('/api/registros', methods=['GET'])
@login_required
def api_listar_registros():
    """API: Listar registros com filtros"""
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        colaborador_id = request.args.get('colaborador_id')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        print(f"\n🔍 Listando registros:")
        print(f"   Data início: {data_inicio}")
        print(f"   Data fim: {data_fim}")
        print(f"   Colaborador: {colaborador_id}")
        print(f"   Página: {page}")
        
        # Construir query
        query = RegistroPonto.query
        
        # Filtros
        if data_inicio:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            query = query.filter(RegistroPonto.data >= data_inicio_dt)
        
        if data_fim:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(RegistroPonto.data <= data_fim_dt)
        
        if colaborador_id:
            query = query.filter(RegistroPonto.colaborador_id == int(colaborador_id))
        
        # Ordenar
        query = query.order_by(
            RegistroPonto.data.desc(),
            RegistroPonto.horario.asc()
        )
        
        # Paginar
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Converter para dict
        registros = [r.to_dict() for r in pagination.items]
        
        # Adicionar nome do colaborador
        for r in registros:
            colaborador = UserMixin.query.get(r['colaborador_id'])
            if colaborador:
                r['colaborador_nome'] = colaborador.username or colaborador.email
        
        print(f"✅ Encontrados {pagination.total} registro(s)")
        
        return jsonify({
            'status': 'success',
            'registros': registros,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        })
        
    except Exception as e:
        print(f"❌ Erro ao listar registros: {e}")
        traceback.print_exc()
        
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@bp.route('/api/resumo-diario', methods=['GET'])
@login_required
def api_resumo_diario():
    """API: Resumo diário com total de horas"""
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        colaborador_id = request.args.get('colaborador_id')
        
        print(f"\n🔍 Buscando resumo diário:")
        print(f"   Data início: {data_inicio}")
        print(f"   Data fim: {data_fim}")
        print(f"   Colaborador: {colaborador_id}")
        
        # Converter datas
        if not data_inicio:
            data_inicio = date.today().strftime('%Y-%m-%d')
        if not data_fim:
            data_fim = date.today().strftime('%Y-%m-%d')
        
        data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        # Buscar registros agrupados por dia
        query = db.session.query(
            RegistroPonto.colaborador_id,
            RegistroPonto.data,
            func.max(RegistroPonto.total_horas).label('total_horas')
        ).filter(
            RegistroPonto.data >= data_inicio_dt,
            RegistroPonto.data <= data_fim_dt
        )
        
        if colaborador_id:
            query = query.filter(RegistroPonto.colaborador_id == int(colaborador_id))
        
        query = query.group_by(
            RegistroPonto.colaborador_id,
            RegistroPonto.data
        ).order_by(
            RegistroPonto.data.desc()
        )
        
        resultados = query.all()
        
        # Montar resumos
        resumos = []
        for r in resultados:
            resumo = RegistroPonto.obter_resumo_dia(r.colaborador_id, r.data)
            
            # Adicionar nome do colaborador
            colaborador = User.query.get(r.colaborador_id)
            if colaborador:
                resumo['colaborador_nome'] = colaborador.username or colaborador.email
            
            resumos.append(resumo)
        
        print(f"✅ Encontrados {len(resumos)} dia(s)")
        
        return jsonify({
            'status': 'success',
            'resumos': resumos,
            'total': len(resumos)
        })
        
    except Exception as e:
        print(f"❌ Erro ao buscar resumo: {e}")
        traceback.print_exc()
        
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@bp.route('/api/colaboradores', methods=['GET'])
@login_required
def api_listar_colaboradores():
    """API: Listar colaboradores ativos"""
    try:
        # Buscar usuários
        colaboradores = User.query.filter_by(active=True).all()
        
        resultado = [{
            'id': c.id,
            'nome': c.username or c.email,
            'email': c.email
        } for c in colaboradores]
        
        return jsonify({
            'status': 'success',
            'colaboradores': resultado,
            'total': len(resultado)
        })
        
    except Exception as e:
        print(f"❌ Erro ao listar colaboradores: {e}")
        
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/home-office/<int:id>/cancelar', methods=['POST'])
@login_required
def api_cancelar_home_office(id):
    """API: Cancelar autorização de home office"""
    from app.models import AutorizacaoHomeOffice
    from app import db
    
    try:
        autorizacao = AutorizacaoHomeOffice.query.get_or_404(id)
        autorizacao.status = 'cancelado'
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Autorização cancelada com sucesso!'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/colaborador/<int:colaborador_id>/auxilio-celular', methods=['GET', 'POST'])
@login_required
def auxilio_celular(colaborador_id):
    """Gerenciar auxílio celular"""
    from app.models import Colaborador, AuxilioCelular
    from app import db
    from datetime import datetime
    
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            # Verificar se já existe
            auxilio = AuxilioCelular.query.filter_by(colaborador_id=colaborador_id).first()
            
            if auxilio:
                auxilio.ativo = data.get('ativo', True)
                auxilio.valor_mensal = data.get('valor_mensal', 50.00)
            else:
                auxilio = AuxilioCelular(
                    colaborador_id=colaborador_id,
                    valor_mensal=data.get('valor_mensal', 50.00),
                    ativo=data.get('ativo', True),
                    data_inicio=datetime.utcnow().date(),
                    motivo_concessao=data.get('motivo_concessao'),
                    criado_por=current_user.id
                )
                db.session.add(auxilio)
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Auxílio celular atualizado com sucesso!'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('rh/auxilio_celular.html', colaborador=colaborador)
