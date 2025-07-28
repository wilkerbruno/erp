from flask import render_template, request, jsonify, make_response
from flask_login import login_required, current_user
from app.blueprints.qualidade import bp
import csv
import io
from datetime import datetime

@bp.route('/')
@login_required
def index():
    return render_template('qualidade/index.html')

@bp.route('/nao-conformidades')
@login_required
def nao_conformidades():
    return render_template('qualidade/nao_conformidades.html')

@bp.route('/nao-conformidades/<int:nc_id>')
@login_required
def ver_nc(nc_id):
    # Dados simulados da NC
    ncs_data = {
        1: {
            'numero': 'NC20250001',
            'titulo': 'Produto fora de especificação',
            'descricao': 'Produto não atendeu aos padrões de qualidade estabelecidos.',
            'origem': 'Interno',
            'criticidade': 'Alta',
            'responsavel': 'João Silva',
            'data_abertura': '20/01/2025',
            'status': 'Em Tratamento'
        },
        2: {
            'numero': 'NC20250002',
            'titulo': 'Atraso na entrega',
            'descricao': 'Produto entregue com atraso de 3 dias.',
            'origem': 'Cliente',
            'criticidade': 'Média',
            'responsavel': 'Maria Santos',
            'data_abertura': '18/01/2025',
            'status': 'Fechada'
        }
    }
    
    nc = ncs_data.get(nc_id, {
        'numero': f'NC{nc_id}',
        'titulo': 'NC não encontrada',
        'descricao': 'Esta NC não foi encontrada no sistema.',
        'origem': '-',
        'criticidade': '-',
        'responsavel': '-',
        'data_abertura': '-',
        'status': 'Não encontrada'
    })
    
    return render_template('qualidade/ver_nc.html', nc=nc, nc_id=nc_id)

@bp.route('/nao-conformidades/<int:nc_id>/editar')
@login_required
def editar_nc(nc_id):
    return f'''
    <h1>Editar NC #{nc_id}</h1>
    <p>Funcionalidade de edição em desenvolvimento.</p>
    <a href="/qualidade/nao-conformidades">Voltar para NCs</a>
    '''

@bp.route('/nao-conformidades/nova')
@login_required
def nova_nc():
    return render_template('qualidade/nova_nc.html')

@bp.route('/nao-conformidades/exportar/<formato>')
@login_required
def exportar_ncs(formato):
    # Dados das NCs para exportar
    ncs = [
        ['NC20250001', 'Produto fora de especificação', 'Interno', 'Alta', 'João Silva', '20/01/2025', 'Em Tratamento'],
        ['NC20250002', 'Atraso na entrega', 'Cliente', 'Média', 'Maria Santos', '18/01/2025', 'Fechada'],
        ['NC20250003', 'Falha no processo', 'Interno', 'Baixa', 'Pedro Costa', '15/01/2025', 'Aberta'],
    ]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if formato == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Numero', 'Titulo', 'Origem', 'Criticidade', 'Responsavel', 'Data', 'Status'])
        writer.writerows(ncs)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=ncs_{timestamp}.csv'
        return response
        
    elif formato == 'excel':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Numero', 'Titulo', 'Origem', 'Criticidade', 'Responsavel', 'Data', 'Status'])
        writer.writerows(ncs)
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = f'attachment; filename=ncs_{timestamp}.xls'
        return response
    
    else:
        return jsonify({'error': 'Formato não suportado'}), 400

@bp.route('/auditorias')
@login_required
def auditorias():
    return render_template('qualidade/auditorias.html')

@bp.route('/indicadores')
@login_required
def indicadores():
    return render_template('qualidade/indicadores.html')
