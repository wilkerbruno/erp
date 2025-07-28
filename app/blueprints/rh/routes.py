from flask import render_template, request, jsonify, make_response, redirect, url_for
from flask_login import login_required, current_user
from app.blueprints.rh import bp
import csv
import io
from datetime import datetime

@bp.route('/')
@login_required
def index():
    return render_template('rh/index.html')

@bp.route('/colaboradores')
@login_required
def colaboradores():
    return render_template('rh/colaboradores.html')

@bp.route('/ponto-eletronico')
@login_required
def ponto_eletronico():
    return render_template('rh/ponto_eletronico.html')

@bp.route('/colaboradores/<int:colaborador_id>')
@login_required
def ver_colaborador(colaborador_id):
    # Dados simulados do colaborador
    colaboradores_data = {
        1: {'nome': 'João Silva Santos', 'cargo': 'Gerente de Produção', 'setor': 'Produção'},
        2: {'nome': 'Maria Santos Lima', 'cargo': 'Supervisora de Qualidade', 'setor': 'Qualidade'},
        3: {'nome': 'Pedro Costa Oliveira', 'cargo': 'Operador de Máquina', 'setor': 'Produção'},
        4: {'nome': 'Ana Silva Rodrigues', 'cargo': 'Analista RH', 'setor': 'RH'}
    }
    
    colaborador = colaboradores_data.get(colaborador_id, {'nome': 'Colaborador não encontrado', 'cargo': '', 'setor': ''})
    return render_template('rh/ver_colaborador.html', colaborador=colaborador, colaborador_id=colaborador_id)

@bp.route('/colaboradores/<int:colaborador_id>/editar')
@login_required
def editar_colaborador(colaborador_id):
    return f'''
    <h1>Editar Colaborador #{colaborador_id}</h1>
    <p>Funcionalidade de edição em desenvolvimento.</p>
    <a href="/rh/colaboradores">Voltar para lista</a>
    '''

@bp.route('/colaboradores/<int:colaborador_id>/historico')
@login_required
def historico_colaborador(colaborador_id):
    return f'''
    <h1>Histórico do Colaborador #{colaborador_id}</h1>
    <p>Histórico de atividades e mudanças do colaborador.</p>
    <a href="/rh/colaboradores">Voltar para lista</a>
    '''

@bp.route('/colaboradores/exportar/<formato>')
@login_required
def exportar_colaboradores(formato):
    # Dados dos colaboradores para exportar
    colaboradores = [
        ['COL000001', 'João Silva Santos', 'joao.silva@empresa.com', 'Gerente de Produção', 'Produção', '15/03/2020', 'Ativo'],
        ['COL000002', 'Maria Santos Lima', 'maria.santos@empresa.com', 'Supervisora de Qualidade', 'Qualidade', '22/08/2019', 'Ativo'],
        ['COL000003', 'Pedro Costa Oliveira', 'pedro.costa@empresa.com', 'Operador de Máquina', 'Produção', '10/01/2022', 'Férias'],
        ['COL000004', 'Ana Silva Rodrigues', 'ana.silva@empresa.com', 'Analista RH', 'RH', '05/06/2021', 'Ativo']
    ]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if formato == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Matricula', 'Nome', 'Email', 'Cargo', 'Setor', 'Admissao', 'Status'])
        writer.writerows(colaboradores)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=colaboradores_{timestamp}.csv'
        return response
        
    elif formato == 'excel':
        # Criar arquivo CSV que pode ser aberto no Excel
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Matricula', 'Nome', 'Email', 'Cargo', 'Setor', 'Admissao', 'Status'])
        writer.writerows(colaboradores)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = f'attachment; filename=colaboradores_{timestamp}.xls'
        return response
        
    elif formato == 'pdf':
        # Criar HTML simples que pode ser salvo como PDF
        html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Lista de Colaboradores</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>Lista de Colaboradores</h1>
    <p>Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
    <table>
        <tr>
            <th>Matrícula</th>
            <th>Nome</th>
            <th>E-mail</th>
            <th>Cargo</th>
            <th>Setor</th>
            <th>Admissão</th>
            <th>Status</th>
        </tr>
'''
        
        for colab in colaboradores:
            html += f'''
        <tr>
            <td>{colab[0]}</td>
            <td>{colab[1]}</td>
            <td>{colab[2]}</td>
            <td>{colab[3]}</td>
            <td>{colab[4]}</td>
            <td>{colab[5]}</td>
            <td>{colab[6]}</td>
        </tr>
'''
        
        html += '''
    </table>
</body>
</html>
'''
        
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename=colaboradores_{timestamp}.html'
        return response
    
    else:
        return jsonify({'error': 'Formato não suportado'}), 400

from flask import send_file, make_response
import csv
import io
from datetime import datetime

@bp.route('/colaboradores/<int:id>/perfil')
@login_required
def perfil_colaborador(id):
    '''Perfil completo do colaborador'''
    return render_template('rh/perfil_colaborador.html', colaborador_id=id)

@bp.route('/colaboradores/<int:id>/editar')
@login_required
def form_editar_colaborador(id):
    '''Formulário de edição do colaborador'''
    return render_template('rh/editar_colaborador.html', colaborador_id=id)

@bp.route('/colaboradores/<int:id>/historico')
@login_required
def historico_colaborador(id):
    '''Histórico completo do colaborador'''
    return render_template('rh/historico_colaborador.html', colaborador_id=id)

@bp.route('/colaboradores/download/<formato>')
@login_required
def download_colaboradores(formato):
    '''Download real de colaboradores'''
    
    # Dados simulados dos colaboradores
    colaboradores_data = [
        {
            'matricula': 'COL000001',
            'nome': 'João Silva Santos',
            'email': 'joao.silva@empresa.com',
            'cargo': 'Gerente de Produção',
            'setor': 'Produção',
            'admissao': '15/03/2020',
            'status': 'Ativo',
            'salario': 'R$ 8.500,00'
        },
        {
            'matricula': 'COL000002',
            'nome': 'Maria Santos Lima',
            'email': 'maria.santos@empresa.com',
            'cargo': 'Supervisora de Qualidade',
            'setor': 'Qualidade',
            'admissao': '22/08/2019',
            'status': 'Ativo',
            'salario': 'R$ 6.200,00'
        },
        {
            'matricula': 'COL000003',
            'nome': 'Pedro Costa Oliveira',
            'email': 'pedro.costa@empresa.com',
            'cargo': 'Operador de Máquina',
            'setor': 'Produção',
            'admissao': '10/01/2022',
            'status': 'Férias',
            'salario': 'R$ 3.800,00'
        },
        {
            'matricula': 'COL000004',
            'nome': 'Ana Silva Rodrigues',
            'email': 'ana.silva@empresa.com',
            'cargo': 'Analista RH',
            'setor': 'RH',
            'admissao': '05/06/2021',
            'status': 'Ativo',
            'salario': 'R$ 4.500,00'
        }
    ]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if formato == 'csv':
        # Gerar CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['matricula', 'nome', 'email', 'cargo', 'setor', 'admissao', 'status', 'salario'])
        writer.writeheader()
        writer.writerows(colaboradores_data)
        
        # Criar resposta
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=colaboradores_{timestamp}.csv'
        return response
        
    elif formato == 'excel':
        # Simular Excel (seria usando openpyxl em produção)
        csv_content = "Matricula,Nome,Email,Cargo,Setor,Admissao,Status,Salario\n"
        for colab in colaboradores_data:
            csv_content += f"{colab['matricula']},{colab['nome']},{colab['email']},{colab['cargo']},{colab['setor']},{colab['admissao']},{colab['status']},{colab['salario']}\n"
        
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = f'attachment; filename=colaboradores_{timestamp}.xls'
        return response
        
    elif formato == 'pdf':
        # Simular PDF (seria usando reportlab em produção)
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Relatório de Colaboradores</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>Relatório de Colaboradores</h1>
            <p>Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
            <table>
                <thead>
                    <tr>
                        <th>Matrícula</th>
                        <th>Nome</th>
                        <th>Cargo</th>
                        <th>Setor</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for colab in colaboradores_data:
            html_content += f'''
                    <tr>
                        <td>{colab['matricula']}</td>
                        <td>{colab['nome']}</td>
                        <td>{colab['cargo']}</td>
                        <td>{colab['setor']}</td>
                        <td>{colab['status']}</td>
                    </tr>
            '''
        
        html_content += '''
                </tbody>
            </table>
        </body>
        </html>
        '''
        
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename=colaboradores_{timestamp}.html'
        return response
    
    else:
        return jsonify({'error': 'Formato não suportado'}), 400

@bp.route('/api/colaborador/<int:id>')
@login_required
def api_colaborador_detalhes(id):
    '''API para detalhes de um colaborador específico'''
    
    # Dados simulados baseados no ID
    colaboradores = {
        1: {
            'id': 1,
            'matricula': 'COL000001',
            'nome': 'João Silva Santos',
            'email': 'joao.silva@empresa.com',
            'telefone': '(11) 98765-4321',
            'cargo': 'Gerente de Produção',
            'setor': 'Produção',
            'admissao': '15/03/2020',
            'status': 'Ativo',
            'salario': 8500.00,
            'endereco': 'Rua das Flores, 123 - São Paulo/SP',
            'cpf': '123.456.789-00',
            'rg': '12.345.678-9'
        },
        2: {
            'id': 2,
            'matricula': 'COL000002',
            'nome': 'Maria Santos Lima',
            'email': 'maria.santos@empresa.com',
            'telefone': '(11) 97654-3210',
            'cargo': 'Supervisora de Qualidade',
            'setor': 'Qualidade',
            'admissao': '22/08/2019',
            'status': 'Ativo',
            'salario': 6200.00,
            'endereco': 'Av. Brasil, 456 - São Paulo/SP',
            'cpf': '987.654.321-00',
            'rg': '98.765.432-1'
        },
        3: {
            'id': 3,
            'matricula': 'COL000003',
            'nome': 'Pedro Costa Oliveira',
            'email': 'pedro.costa@empresa.com',
            'telefone': '(11) 96543-2109',
            'cargo': 'Operador de Máquina',
            'setor': 'Produção',
            'admissao': '10/01/2022',
            'status': 'Férias',
            'salario': 3800.00,
            'endereco': 'Rua do Trabalho, 789 - São Paulo/SP',
            'cpf': '456.789.123-00',
            'rg': '45.678.912-3'
        },
        4: {
            'id': 4,
            'matricula': 'COL000004',
            'nome': 'Ana Silva Rodrigues',
            'email': 'ana.silva@empresa.com',
            'telefone': '(11) 95432-1098',
            'cargo': 'Analista RH',
            'setor': 'RH',
            'admissao': '05/06/2021',
            'status': 'Ativo',
            'salario': 4500.00,
            'endereco': 'Rua dos Recursos, 321 - São Paulo/SP',
            'cpf': '789.123.456-00',
            'rg': '78.912.345-6'
        }
    }
    
    colaborador = colaboradores.get(id)
    if colaborador:
        return jsonify(colaborador)
    else:
        return jsonify({'error': 'Colaborador não encontrado'}), 404
