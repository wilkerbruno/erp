from flask import render_template, request, jsonify
from flask_login import login_required
from app.blueprints.rh import bp
from datetime import datetime
from io import BytesIO
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, send_file


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
    return render_template('rh/ponto/gerenciar.html')

@bp.route('/controle-ponto')
@login_required
def controle_ponto():
    """Controle geral de ponto"""
    return render_template('rh/ponto/controle.html')


@bp.route('/api/registrar-ponto', methods=['POST'])
@login_required
def api_registrar_ponto():
    """API: Registrar ponto - SEMPRE retorna JSON"""
    # Envolver TUDO em try-catch para garantir que sempre retorna JSON
    try:
        # Log para debug
        print("\n" + "="*60)
        print("🔍 API Registrar Ponto chamada")
        print(f"Method: {request.method}")
        print(f"Content-Type: {request.content_type}")
        print(f"Is JSON: {request.is_json}")
        
        # Tentar obter dados de múltiplas formas
        data = None
        
        if request.is_json:
            data = request.get_json()
            print(f"✅ Dados via get_json(): {data}")
        elif request.data:
            import json
            try:
                data = json.loads(request.data.decode('utf-8'))
                print(f"✅ Dados via json.loads(): {data}")
            except:
                print("⚠️ Falha ao fazer parse do JSON")
        
        if not data and request.form:
            data = dict(request.form)
            print(f"✅ Dados via form: {data}")
        
        # Se não tem dados, retornar JSON de erro
        if not data or len(data) == 0:
            print("❌ Nenhum dado recebido!")
            response = jsonify({
                'status': 'error',
                'message': 'Nenhum dado foi enviado na requisição'
            })
            response.headers['Content-Type'] = 'application/json'
            return response, 400
        
        print(f"📦 Dados recebidos: {data}")
        
        # Adicionar valores padrão para campos faltantes
        if 'colaborador_id' not in data or not data['colaborador_id']:
            data['colaborador_id'] = 1
            print(f"⚠️ colaborador_id não enviado, usando padrão: 1")
        
        if 'data' not in data or not data['data']:
            from datetime import date
            data['data'] = str(date.today())
            print(f"⚠️ data não enviada, usando hoje: {data['data']}")
        
        if 'horario' not in data or not data['horario']:
            from datetime import datetime
            data['horario'] = datetime.now().strftime('%H:%M:%S')
            print(f"⚠️ horario não enviado, usando agora: {data['horario']}")
        
        # Verificar campo obrigatório: tipo
        if 'tipo' not in data or not data['tipo']:
            print("❌ Campo 'tipo' é obrigatório!")
            response = jsonify({
                'status': 'error',
                'message': 'Campo "tipo" é obrigatório (entrada, saida, etc)'
            })
            response.headers['Content-Type'] = 'application/json'
            return response, 400
        
        print(f"✅ Tipo de ponto: {data['tipo']}")
        
        # Calcular atraso se for entrada
        atraso_minutos = 0
        if data['tipo'] == 'entrada':
            from datetime import datetime, date
            try:
                horario_entrada = datetime.strptime(data['horario'], '%H:%M:%S').time()
                horario_esperado = datetime.strptime('08:00:00', '%H:%M:%S').time()
                
                if horario_entrada > horario_esperado:
                    delta = datetime.combine(date.today(), horario_entrada) - datetime.combine(date.today(), horario_esperado)
                    atraso_minutos = int(delta.total_seconds() / 60)
                    print(f"⚠️ Atraso detectado: {atraso_minutos} minutos")
            except Exception as e:
                print(f"⚠️ Erro ao calcular atraso: {e}")
        
        # Construir resposta de sucesso
        response_data = {
            'status': 'success',
            'message': 'Ponto registrado com sucesso!',
            'atraso_minutos': atraso_minutos,
            'home_office_autorizado': data.get('home_office', False),
            'registro': {
                'tipo': data['tipo'],
                'horario': data['horario'],
                'data': data['data'],
                'colaborador_id': data['colaborador_id']
            }
        }
        
        print(f"✅ Sucesso! Retornando JSON")
        print("="*60 + "\n")
        
        response = jsonify(response_data)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    except Exception as e:
        # CRÍTICO: Garantir que mesmo em exceção retorna JSON
        import traceback
        error_traceback = traceback.format_exc()
        print(f"\n❌ EXCEÇÃO CAPTURADA:")
        print(error_traceback)
        print("="*60 + "\n")
        
        response = jsonify({
            'status': 'error',
            'message': f'Erro no servidor: {str(e)}',
            'error_type': type(e).__name__
        })
        response.headers['Content-Type'] = 'application/json'
        return response, 500


@bp.route('/api/ponto/hoje/<int:colaborador_id>')
@login_required
def api_ponto_hoje(colaborador_id):
    """API: Obter registros de ponto de hoje - SEMPRE retorna JSON"""
    try:
        print(f"\n🔍 Consultando pontos de hoje para colaborador {colaborador_id}")
        
        from datetime import date
        hoje = date.today()
        
        # Mock data para teste (substitua por consulta ao banco depois)
        registros = []
        
        # Exemplo de registro (descomente para testar):
        # registros = [
        #     {
        #         'tipo': 'entrada',
        #         'horario': '08:05:00',
        #         'data': str(hoje),
        #         'home_office': False,
        #         'atraso_minutos': 5,
        #         'dentro_horario': False
        #     }
        # ]
        
        print(f"✅ Retornando {len(registros)} registro(s)")
        
        response = jsonify({
            'status': 'success',
            'registros': registros,
            'data': str(hoje),
            'colaborador_id': colaborador_id
        })
        response.headers['Content-Type'] = 'application/json'
        return response
        
    except Exception as e:
        print(f"❌ Erro ao consultar pontos: {e}")
        
        response = jsonify({
            'status': 'error',
            'message': str(e),
            'registros': []
        })
        response.headers['Content-Type'] = 'application/json'
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


