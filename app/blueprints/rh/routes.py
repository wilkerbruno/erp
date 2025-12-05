from flask import render_template, request, jsonify
from flask_login import login_required
from app.blueprints.rh import bp
from datetime import datetime
from io import BytesIO
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, send_file
from app import db
from app.models.registros_ponto import RegistroPonto, AutorizacaoHomeOffice
from sqlalchemy import and_


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
    """Ver detalhes do colaborador"""
    colaborador = {
        'id': colaborador_id,
        'nome': 'João Silva',
        'cargo': 'Analista',
        'departamento': 'TI',
        'email': 'joao@empresa.com'
    }
    return render_template('rh/ver_colaborador.html', colaborador=colaborador)

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
    """Criar novo benefício"""
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            # Aqui você implementaria a lógica de criação
            # Por enquanto, retorno de sucesso
            
            return jsonify({
                'status': 'success',
                'message': 'Benefício criado com sucesso!'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('rh/beneficios/novo.html')

@bp.route('/api/beneficios')
@login_required
def api_listar_beneficios():
    """API: Lista todos os benefícios"""
    # Mock de dados para não dar erro
    beneficios = [
        {
            'id': 1,
            'nome': 'Vale Alimentação',
            'tipo': 'fixo',
            'valor': 500.00,
            'ativo': True
        },
        {
            'id': 2,
            'nome': 'Auxílio Celular',
            'tipo': 'fixo',
            'valor': 50.00,
            'ativo': True
        }
    ]
    
    return jsonify({
        'status': 'success',
        'beneficios': beneficios
    })





# ========== PONTO ELETRÔNICO ==========
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
    return render_template('rh/ponto/controle.html')


@bp.route('/api/registrar-ponto', methods=['POST'])
@login_required
def api_registrar_ponto():
    """API: Registrar ponto - USA DATA DO SERVIDOR"""
    try:
        print("\n" + "="*60)
        print("🔍 API Registrar Ponto chamada")
        
        # Obter dados
        data = None
        if request.is_json:
            data = request.get_json()
        elif request.data:
            try:
                data = json.loads(request.data.decode('utf-8'))
            except:
                pass
        
        if not data:
            data = dict(request.form) if request.form else {}
        
        if not data:
            print("❌ Nenhum dado recebido!")
            response = jsonify({
                'status': 'error',
                'message': 'Nenhum dado foi enviado'
            })
            response.headers['Content-Type'] = 'application/json'
            return response, 400
        
        print(f"📦 Dados recebidos: {data}")
        
        # ✅ SEMPRE USAR DATA E HORA DO SERVIDOR
        colaborador_id = data.get('colaborador_id', current_user.id)
        
        # IGNORAR data e horario do cliente, usar do servidor
        agora = datetime.now()
        data_registro = agora.date()  # Date object
        horario_registro = agora.time()  # Time object
        
        print(f"⏰ Data/Hora do SERVIDOR: {data_registro} {horario_registro}")
        print(f"   (Ignorando data do cliente: {data.get('data')})")
        
        # Validar tipo
        tipo = data.get('tipo')
        if not tipo:
            response = jsonify({
                'status': 'error',
                'message': 'Campo "tipo" é obrigatório'
            })
            response.headers['Content-Type'] = 'application/json'
            return response, 400
        
        # Calcular atraso
        atraso_minutos = 0
        if tipo == 'entrada':
            try:
                horario_esperado = datetime.strptime('08:00:00', '%H:%M:%S').time()
                if horario_registro > horario_esperado:
                    delta = datetime.combine(date.today(), horario_registro) - datetime.combine(date.today(), horario_esperado)
                    atraso_minutos = int(delta.total_seconds() / 60)
                    print(f"⚠️ Atraso detectado: {atraso_minutos} minutos")
            except Exception as e:
                print(f"⚠️ Erro ao calcular atraso: {e}")
        
        # Verificar autorização de home office
        home_office = data.get('home_office', False)
        home_office_autorizado = False
        
        if home_office:
            home_office_autorizado = AutorizacaoHomeOffice.verificar_autorizacao(
                colaborador_id, 
                data_registro
            )
            print(f"🏠 Home Office autorizado: {home_office_autorizado}")
        
        # Obter IP do cliente
        ip_address = request.remote_addr
        
        # ✅ SALVAR NO BANCO
        try:
            novo_registro = RegistroPonto(
                colaborador_id=colaborador_id,
                data=data_registro,  # Date do servidor
                horario=horario_registro,  # Time do servidor
                tipo=tipo,
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                localizacao_texto=data.get('localizacao_texto', data.get('endereco', '')),
                home_office=home_office,
                home_office_autorizado=home_office_autorizado,
                atraso_minutos=atraso_minutos,
                dispositivo=data.get('dispositivo', request.user_agent.string),
                ip_address=ip_address
            )
            
            db.session.add(novo_registro)
            db.session.commit()
            
            print(f"✅ Registro salvo no banco! ID: {novo_registro.id}")
            print(f"   Colaborador: {colaborador_id}")
            print(f"   Data: {data_registro}")
            print(f"   Horário: {horario_registro}")
            print(f"   Tipo: {tipo}")
            print(f"   Atraso: {atraso_minutos} min")
            
        except Exception as e_db:
            print(f"❌ Erro ao salvar no banco: {e_db}")
            db.session.rollback()
            
            response = jsonify({
                'status': 'error',
                'message': f'Erro ao salvar no banco: {str(e_db)}'
            })
            response.headers['Content-Type'] = 'application/json'
            return response, 500
        
        # Resposta de sucesso
        print(f"✅ Sucesso! Tipo: {tipo}")
        print("="*60 + "\n")
        
        response = jsonify({
            'status': 'success',
            'message': 'Ponto registrado com sucesso!',
            'atraso_minutos': atraso_minutos,
            'home_office_autorizado': home_office_autorizado,
            'registro': {
                'id': novo_registro.id,
                'tipo': tipo,
                'horario': str(horario_registro),
                'data': str(data_registro),
                'atraso_minutos': atraso_minutos,
                'dentro_horario': atraso_minutos == 0,
                'home_office': home_office,
                'home_office_autorizado': home_office_autorizado
            }
        })
        response.headers['Content-Type'] = 'application/json'
        return response
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"\n❌ ERRO:")
        print(error_traceback)
        
        response = jsonify({
            'status': 'error',
            'message': str(e)
        })
        response.headers['Content-Type'] = 'application/json'
        return response, 500


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
    """API: Autorizar home office para colaborador"""
    try:
        data = request.get_json()
        
        # Mock de resposta
        return jsonify({
            'status': 'success',
            'message': 'Home office autorizado com sucesso!',
            'autorizacao': {
                'id': 1,
                'colaborador_id': data.get('colaborador_id'),
                'data_inicio': data.get('data_inicio'),
                'data_fim': data.get('data_fim')
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/api/home-office/listar')
@login_required
def api_listar_home_office():
    """API: Listar autorizações de home office"""
    # Mock de dados
    autorizacoes = [
        {
            'id': 1,
            'colaborador': 'João Silva',
            'data_inicio': '2024-01-15',
            'data_fim': '2024-01-19',
            'status': 'ativo'
        }
    ]
    
    return jsonify({
        'status': 'success',
        'autorizacoes': autorizacoes
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
    """API: Gerar holerite para colaborador"""
    try:
        data = request.get_json()
        
        # Mock de resposta
        return jsonify({
            'status': 'success',
            'message': 'Holerite gerado com sucesso!',
            'holerite': {
                'id': 1,
                'colaborador_id': data.get('colaborador_id'),
                'mes': data.get('mes'),
                'ano': data.get('ano'),
                'salario_base': data.get('salario_base', 0),
                'total_vencimentos': data.get('salario_base', 0),
                'total_descontos': 0,
                'liquido': data.get('salario_base', 0)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/api/holerite/listar')
@login_required
def api_listar_holerites():
    """API: Listar holerites"""
    # Mock de dados
    holerites = [
        {
            'id': 1,
            'colaborador': 'João Silva',
            'mes': 1,
            'ano': 2024,
            'liquido': 2500.00
        }
    ]
    
    return jsonify({
        'status': 'success',
        'holerites': holerites
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
    """API: Importar DRE do contador"""
    try:
        # Mock de resposta
        return jsonify({
            'status': 'success',
            'message': 'DRE importada com sucesso!',
            'dre': {
                'id': 1,
                'mes': request.form.get('mes', 1),
                'ano': request.form.get('ano', 2024),
                'receita_bruta': 100000.00,
                'receita_liquida': 90000.00,
                'lucro_bruto': 50000.00,
                'resultado_liquido': 30000.00
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

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


