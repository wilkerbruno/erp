from flask import render_template, request, jsonify, make_response, flash, redirect, url_for
from flask_login import login_required, current_user
from app.blueprints.empresas import bp
import csv
import io
from datetime import datetime

@bp.route('/')
@login_required
def index():
    return render_template('empresas/index.html')

@bp.route('/nova')
@login_required
def nova_empresa():
    return render_template('empresas/nova_empresa.html')

@bp.route('/empresas/<int:empresa_id>')
@login_required
def ver_empresa(empresa_id):
    # Dados simulados da empresa
    empresas_data = {
        1: {
            'id': 1,
            'razao_social': 'Indústria ABC Ltda',
            'nome_fantasia': 'ABC Indústrias',
            'cnpj': '12.345.678/0001-90',
            'inscricao_estadual': '123.456.789.012',
            'endereco': 'Rua Industrial, 1000',
            'cidade': 'São Paulo',
            'uf': 'SP',
            'cep': '01234-567',
            'telefone': '(11) 3456-7890',
            'email': 'contato@abc.com.br',
            'responsavel': 'João Silva',
            'setor': 'Metalúrgica',
            'funcionarios': 250,
            'faturamento': 15000000.00,
            'data_cadastro': '15/01/2023',
            'status': 'Ativo'
        },
        2: {
            'id': 2,
            'razao_social': 'Tecnologia XYZ S.A.',
            'nome_fantasia': 'XYZ Tech',
            'cnpj': '98.765.432/0001-10',
            'inscricao_estadual': '987.654.321.098',
            'endereco': 'Av. Tecnológica, 500',
            'cidade': 'São Paulo',
            'uf': 'SP',
            'cep': '04567-890',
            'telefone': '(11) 9876-5432',
            'email': 'info@xyztech.com.br',
            'responsavel': 'Maria Santos',
            'setor': 'Tecnologia',
            'funcionarios': 120,
            'faturamento': 8500000.00,
            'data_cadastro': '22/03/2023',
            'status': 'Ativo'
        }
    }
    
    empresa = empresas_data.get(empresa_id, {
        'razao_social': 'Empresa não encontrada',
        'status': 'Não encontrada'
    })
    
    return render_template('empresas/ver_empresa.html', empresa=empresa, empresa_id=empresa_id)

@bp.route('/empresas/<int:empresa_id>/editar')
@login_required
def editar_empresa(empresa_id):
    return render_template('empresas/editar_empresa.html', empresa_id=empresa_id)

@bp.route('/salvar', methods=['POST'])
@login_required
def salvar_empresa():
    try:
        dados = request.get_json()
        # Aqui seria a lógica para salvar no banco
        empresa_id = 100 + int(str(hash(dados.get('cnpj', '')))[-3:])
        
        return jsonify({
            'success': True,
            'message': f'Empresa {dados.get("razao_social")} cadastrada com sucesso!',
            'empresa_id': empresa_id
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/buscar')
@login_required
def buscar_empresas():
    termo = request.args.get('q', '')
    
    # Dados simulados de busca
    todas_empresas = [
        {'id': 1, 'razao_social': 'Indústria ABC Ltda', 'cnpj': '12.345.678/0001-90', 'cidade': 'São Paulo'},
        {'id': 2, 'razao_social': 'Tecnologia XYZ S.A.', 'cnpj': '98.765.432/0001-10', 'cidade': 'São Paulo'},
        {'id': 3, 'razao_social': 'Comércio DEF Ltda', 'cnpj': '11.222.333/0001-44', 'cidade': 'Rio de Janeiro'},
        {'id': 4, 'razao_social': 'Serviços GHI Ltda', 'cnpj': '55.666.777/0001-88', 'cidade': 'Belo Horizonte'}
    ]
    
    if termo:
        empresas_filtradas = [
            emp for emp in todas_empresas 
            if termo.lower() in emp['razao_social'].lower() or termo in emp['cnpj']
        ]
    else:
        empresas_filtradas = todas_empresas
    
    return jsonify(empresas_filtradas)

@bp.route('/exportar/<formato>')
@login_required
def exportar_empresas(formato):
    # Dados das empresas para exportar
    empresas = [
        ['12.345.678/0001-90', 'Indústria ABC Ltda', 'ABC Indústrias', 'São Paulo', 'SP', '(11) 3456-7890', 'Ativo'],
        ['98.765.432/0001-10', 'Tecnologia XYZ S.A.', 'XYZ Tech', 'São Paulo', 'SP', '(11) 9876-5432', 'Ativo'],
        ['11.222.333/0001-44', 'Comércio DEF Ltda', 'DEF Comércio', 'Rio de Janeiro', 'RJ', '(21) 1111-2222', 'Ativo'],
    ]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if formato == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['CNPJ', 'Razao Social', 'Nome Fantasia', 'Cidade', 'UF', 'Telefone', 'Status'])
        writer.writerows(empresas)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=empresas_{timestamp}.csv'
        return response
        
    elif formato == 'excel':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['CNPJ', 'Razao Social', 'Nome Fantasia', 'Cidade', 'UF', 'Telefone', 'Status'])
        writer.writerows(empresas)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = f'attachment; filename=empresas_{timestamp}.xls'
        return response
    
    else:
        return jsonify({'error': 'Formato não suportado'}), 400

@bp.route('/api/consulta-cnpj/<cnpj>')
@login_required
def consulta_cnpj(cnpj):
    # Simulação de consulta de CNPJ (em produção usaria API da Receita)
    cnpjs_mock = {
        '12345678000190': {
            'razao_social': 'EMPRESA EXEMPLO LTDA',
            'nome_fantasia': 'Exemplo Empresa',
            'endereco': 'RUA EXEMPLO, 123',
            'cidade': 'SAO PAULO',
            'uf': 'SP',
            'cep': '01234567',
            'telefone': '(11) 1234-5678',
            'situacao': 'ATIVA'
        }
    }
    
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    dados = cnpjs_mock.get(cnpj_limpo, {})
    
    if dados:
        return jsonify({'success': True, 'dados': dados})
    else:
        return jsonify({'success': False, 'message': 'CNPJ não encontrado'})
