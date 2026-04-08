from flask import render_template, request, jsonify, make_response
from flask_login import login_required
from app import app, csrf
import csv
import io
from datetime import datetime


@app.route('/empresas/')
@login_required
def empresas_index():
    return render_template('empresas/index.html')


@app.route('/empresas/nova')
@login_required
def empresas_nova():
    return render_template('empresas/nova_empresa.html')


@app.route('/empresas/<int:empresa_id>')
@login_required
def empresas_ver(empresa_id):
    empresas_data = {
        1: {
            'id': 1,
            'razao_social': 'Industria ABC Ltda',
            'nome_fantasia': 'ABC Industrias',
            'cnpj': '12.345.678/0001-90',
            'inscricao_estadual': '123.456.789.012',
            'endereco': 'Rua Industrial, 1000',
            'cidade': 'Sao Paulo',
            'uf': 'SP',
            'cep': '01234-567',
            'telefone': '(11) 3456-7890',
            'email': 'contato@abc.com.br',
            'responsavel': 'Joao Silva',
            'setor': 'Metalurgica',
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
            'endereco': 'Av. Tecnologica, 500',
            'cidade': 'Sao Paulo',
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
        'razao_social': 'Empresa nao encontrada',
        'status': 'Nao encontrada'
    })
    return render_template('empresas/ver_empresa.html', empresa=empresa, empresa_id=empresa_id)


@app.route('/empresas/<int:empresa_id>/editar')
@login_required
def empresas_editar(empresa_id):
    return render_template('empresas/editar_empresa.html', empresa_id=empresa_id)


@app.route('/empresas/salvar', methods=['POST'])
@login_required
@csrf.exempt
def empresas_salvar():
    try:
        dados = request.get_json()
        empresa_id = 100 + abs(hash(dados.get('cnpj', ''))) % 900
        return jsonify({
            'success': True,
            'message': f'Empresa {dados.get("razao_social")} cadastrada com sucesso!',
            'empresa_id': empresa_id
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/empresas/buscar')
@login_required
def empresas_buscar():
    termo = request.args.get('q', '')
    todas = [
        {'id': 1, 'razao_social': 'Industria ABC Ltda', 'cnpj': '12.345.678/0001-90', 'cidade': 'Sao Paulo'},
        {'id': 2, 'razao_social': 'Tecnologia XYZ S.A.', 'cnpj': '98.765.432/0001-10', 'cidade': 'Sao Paulo'},
        {'id': 3, 'razao_social': 'Comercio DEF Ltda', 'cnpj': '11.222.333/0001-44', 'cidade': 'Rio de Janeiro'},
        {'id': 4, 'razao_social': 'Servicos GHI Ltda', 'cnpj': '55.666.777/0001-88', 'cidade': 'Belo Horizonte'}
    ]
    if termo:
        resultado = [e for e in todas if termo.lower() in e['razao_social'].lower() or termo in e['cnpj']]
    else:
        resultado = todas
    return jsonify(resultado)


@app.route('/empresas/exportar/<formato>')
@login_required
def empresas_exportar(formato):
    empresas = [
        ['12.345.678/0001-90', 'Industria ABC Ltda', 'ABC Industrias', 'Sao Paulo', 'SP', '(11) 3456-7890', 'Ativo'],
        ['98.765.432/0001-10', 'Tecnologia XYZ S.A.', 'XYZ Tech', 'Sao Paulo', 'SP', '(11) 9876-5432', 'Ativo'],
        ['11.222.333/0001-44', 'Comercio DEF Ltda', 'DEF Comercio', 'Rio de Janeiro', 'RJ', '(21) 1111-2222', 'Ativo'],
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

    return jsonify({'error': 'Formato nao suportado'}), 400


@app.route('/empresas/api/consulta-cnpj/<cnpj>')
@login_required
def empresas_consulta_cnpj(cnpj):
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
    return jsonify({'success': False, 'message': 'CNPJ nao encontrado'})