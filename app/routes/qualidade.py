from flask import render_template, request, jsonify, make_response
from flask_login import login_required
from app import app
import csv
import io
from datetime import datetime


@app.route('/qualidade/')
@login_required
def qualidade_index():
    return render_template('qualidade/index.html')


@app.route('/qualidade/nao-conformidades')
@login_required
def qualidade_nao_conformidades():
    return render_template('qualidade/nao_conformidades.html')


@app.route('/qualidade/nao-conformidades/<int:nc_id>')
@login_required
def qualidade_ver_nc(nc_id):
    ncs_data = {
        1: {
            'numero': 'NC20250001',
            'titulo': 'Produto fora de especificacao',
            'descricao': 'Produto nao atendeu aos padroes de qualidade estabelecidos.',
            'origem': 'Interno',
            'criticidade': 'Alta',
            'responsavel': 'Joao Silva',
            'data_abertura': '20/01/2025',
            'status': 'Em Tratamento'
        },
        2: {
            'numero': 'NC20250002',
            'titulo': 'Atraso na entrega',
            'descricao': 'Produto entregue com atraso de 3 dias.',
            'origem': 'Cliente',
            'criticidade': 'Media',
            'responsavel': 'Maria Santos',
            'data_abertura': '18/01/2025',
            'status': 'Fechada'
        }
    }
    nc = ncs_data.get(nc_id, {
        'numero': f'NC{nc_id}',
        'titulo': 'NC nao encontrada',
        'descricao': 'Esta NC nao foi encontrada no sistema.',
        'origem': '-',
        'criticidade': '-',
        'responsavel': '-',
        'data_abertura': '-',
        'status': 'Nao encontrada'
    })
    return render_template('qualidade/ver_nc.html', nc=nc, nc_id=nc_id)


@app.route('/qualidade/nao-conformidades/<int:nc_id>/editar')
@login_required
def qualidade_editar_nc(nc_id):
    return render_template('qualidade/editar_nc.html', nc_id=nc_id)


@app.route('/qualidade/nao-conformidades/nova')
@login_required
def qualidade_nova_nc():
    return render_template('qualidade/nova_nc.html')


@app.route('/qualidade/nao-conformidades/exportar/<formato>')
@login_required
def qualidade_exportar_ncs(formato):
    ncs = [
        ['NC20250001', 'Produto fora de especificacao', 'Interno', 'Alta', 'Joao Silva', '20/01/2025', 'Em Tratamento'],
        ['NC20250002', 'Atraso na entrega', 'Cliente', 'Media', 'Maria Santos', '18/01/2025', 'Fechada'],
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

    return jsonify({'error': 'Formato nao suportado'}), 400


@app.route('/qualidade/auditorias')
@login_required
def qualidade_auditorias():
    return render_template('qualidade/auditorias.html')


@app.route('/qualidade/indicadores')
@login_required
def qualidade_indicadores():
    return render_template('qualidade/indicadores.html')