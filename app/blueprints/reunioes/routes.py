from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.blueprints.reunioes import bp

@bp.route('/')
@login_required
def index():
    """Dashboard principal de Reuniões"""
    return render_template('reunioes/index.html')

@bp.route('/agenda')
@login_required
def agenda():
    """Agenda de Reuniões"""
    return render_template('reunioes/agenda.html')

@bp.route('/atas')
@login_required
def atas():
    """Gestão de Atas"""
    return render_template('reunioes/atas.html')

@bp.route('/participantes')
@login_required
def participantes():
    """Gestão de Participantes"""
    return render_template('reunioes/participantes.html')

@bp.route('/acoes')
@login_required
def acoes():
    """Acompanhamento de Ações"""
    return render_template('reunioes/acoes.html')

@bp.route('/salas')
@login_required
def salas():
    """Gestão de Salas"""
    return render_template('reunioes/salas.html')

@bp.route('/nova-reuniao')
@login_required
def nova_reuniao():
    """Agendar Nova Reunião"""
    return render_template('reunioes/nova_reuniao.html')

# APIs
@bp.route('/api/reuniao/criar', methods=['POST'])
@login_required
def api_criar_reuniao():
    """API para criar nova reunião"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Reunião agendada com sucesso!',
            'reuniao_id': 123
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar reunião: {str(e)}'
        }), 500

@bp.route('/api/ata/criar', methods=['POST'])
@login_required
def api_criar_ata():
    """API para criar nova ata"""
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Ata criada com sucesso!',
            'ata_id': 456
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao criar ata: {str(e)}'
        }), 500
