from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.blueprints.consultoria import bp

@bp.route('/')
@login_required
def index():
    """Dashboard principal da Consultoria"""
    return render_template('consultoria/index.html')

@bp.route('/projetos')
@login_required
def projetos():
    """Gestão de Projetos de Consultoria"""
    return render_template('consultoria/projetos.html')

@bp.route('/clientes')
@login_required
def clientes():
    """Gestão de Clientes"""
    return render_template('consultoria/clientes.html')

@bp.route('/consultores')
@login_required
def consultores():
    """Gestão de Consultores"""
    return render_template('consultoria/consultores.html')

@bp.route('/contratos')
@login_required
def contratos():
    """Gestão de Contratos"""
    return render_template('consultoria/contratos.html')

@bp.route('/cronogramas')
@login_required
def cronogramas():
    """Cronogramas de Projetos"""
    return render_template('consultoria/cronogramas.html')

@bp.route('/novo-projeto')
@login_required
def novo_projeto():
    """Criar Novo Projeto"""
    return render_template('consultoria/novo_projeto.html')

# APIs
@bp.route('/api/projeto/criar', methods=['POST'])
@login_required
def api_criar_projeto():
    """API para criar novo projeto"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Projeto criado com sucesso!',
            'projeto_id': 123
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar projeto: {str(e)}'
        }), 500

@bp.route('/api/cliente/criar', methods=['POST'])
@login_required
def api_criar_cliente():
    """API para criar novo cliente"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Cliente cadastrado com sucesso!',
            'cliente_id': 456
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar cliente: {str(e)}'
        }), 500
