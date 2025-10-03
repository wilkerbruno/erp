"""
Rotas para Sistema de Permissões e Níveis de Acesso
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Role, Permissao, NivelAcesso, Colaborador, Cargo, Departamento

permissoes_bp = Blueprint('permissoes', __name__, url_prefix='/rh/permissoes')

# Decorator para verificar permissões
def requer_permissao(codigo_permissao):
    """Decorator para verificar se usuário tem permissão"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.tem_permissao(codigo_permissao):
                flash('Você não tem permissão para acessar esta funcionalidade.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ===== ROTAS DE VISUALIZAÇÃO =====

@permissoes_bp.route('/')
@login_required
@requer_permissao('permissoes.visualizar')
def index():
    """Página principal de gestão de permissões"""
    return render_template('rh/permissoes/index.html')

@permissoes_bp.route('/roles')
@login_required
@requer_permissao('roles.visualizar')
def listar_roles():
    """Lista todos os roles"""
    return render_template('rh/permissoes/roles.html')

@permissoes_bp.route('/colaborador/<int:colaborador_id>/nivel-acesso')
@login_required
@requer_permissao('nivel_acesso.gerenciar')
def configurar_nivel_acesso(colaborador_id):
    """Configura nível de acesso de um colaborador"""
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    return render_template('rh/permissoes/nivel_acesso.html', colaborador=colaborador)

# ===== APIs DE ROLES =====

@permissoes_bp.route('/api/roles', methods=['GET'])
@login_required
@requer_permissao('roles.visualizar')
def api_listar_roles():
    """API: Lista todos os roles"""
    roles = Role.query.filter_by(ativo=True).all()
    return jsonify({
        'status': 'success',
        'roles': [r.to_dict() for r in roles]
    })

@permissoes_bp.route('/api/roles', methods=['POST'])
@login_required
@requer_permissao('roles.criar')
def api_criar_role():
    """API: Cria novo role"""
    data = request.get_json()
    
    try:
        role = Role(
            nome=data['nome'],
            codigo=data['codigo'],
            descricao=data.get('descricao'),
            nivel_hierarquico=data.get('nivel_hierarquico', 0)
        )
        
        db.session.add(role)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Role criado com sucesso',
            'role': role.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@permissoes_bp.route('/api/roles/<int:role_id>/permissoes', methods=['POST'])
@login_required
@requer_permissao('roles.editar')
def api_atribuir_permissoes_role(role_id):
    """API: Atribui permissões a um role"""
    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    
    try:
        permissoes_ids = data.get('permissoes_ids', [])
        permissoes = Permissao.query.filter(Permissao.id.in_(permissoes_ids)).all()
        
        role.permissoes = permissoes
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Permissões atribuídas com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# ===== APIs DE PERMISSÕES =====

@permissoes_bp.route('/api/permissoes', methods=['GET'])
@login_required
@requer_permissao('permissoes.visualizar')
def api_listar_permissoes():
    """API: Lista todas as permissões"""
    permissoes = Permissao.query.filter_by(ativo=True).all()
    
    # Agrupar por módulo
    permissoes_por_modulo = {}
    for p in permissoes:
        modulo = p.modulo or 'geral'
        if modulo not in permissoes_por_modulo:
            permissoes_por_modulo[modulo] = []
        permissoes_por_modulo[modulo].append(p.to_dict())
    
    return jsonify({
        'status': 'success',
        'permissoes': permissoes_por_modulo
    })

# ===== APIs DE NÍVEL DE ACESSO =====

@permissoes_bp.route('/api/nivel-acesso/<int:colaborador_id>', methods=['GET'])
@login_required
@requer_permissao('nivel_acesso.visualizar')
def api_obter_nivel_acesso(colaborador_id):
    """API: Obtém nível de acesso de um colaborador"""
    nivel = NivelAcesso.query.filter_by(colaborador_id=colaborador_id).first()
    
    if nivel:
        return jsonify({
            'status': 'success',
            'nivel_acesso': nivel.to_dict()
        })
    else:
        return jsonify({
            'status': 'success',
            'nivel_acesso': None
        })

@permissoes_bp.route('/api/nivel-acesso/<int:colaborador_id>', methods=['POST'])
@login_required
@requer_permissao('nivel_acesso.gerenciar')
def api_configurar_nivel_acesso(colaborador_id):
    """API: Configura nível de acesso de um colaborador"""
    colaborador = Colaborador.query.get_or_404(colaborador_id)
    data = request.get_json()
    
    try:
        # Verificar se já existe nível de acesso
        nivel = NivelAcesso.query.filter_by(colaborador_id=colaborador_id).first()
        
        if nivel:
            # Atualizar existente
            nivel.tipo_acesso = data.get('tipo_acesso')
            nivel.modulos_liberados = data.get('modulos_liberados', [])
            nivel.restricoes = data.get('restricoes', {})
            nivel.data_fim = data.get('data_fim')
            nivel.ativo = data.get('ativo', True)
        else:
            # Criar novo
            nivel = NivelAcesso(
                colaborador_id=colaborador_id,
                tipo_acesso=data.get('tipo_acesso'),
                modulos_liberados=data.get('modulos_liberados', []),
                restricoes=data.get('restricoes', {}),
                data_fim=data.get('data_fim'),
                criado_por=current_user.id
            )
            db.session.add(nivel)
        
        # Atribuir roles ao usuário do colaborador
        if colaborador.usuario_id and data.get('roles_ids'):
            from app.models import User
            usuario = User.query.get(colaborador.usuario_id)
            if usuario:
                roles = Role.query.filter(Role.id.in_(data['roles_ids'])).all()
                usuario.roles = roles
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Nível de acesso configurado com sucesso',
            'nivel_acesso': nivel.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# ===== APIs DE CARGO/DEPARTAMENTO =====

@permissoes_bp.route('/api/cargo/<int:cargo_id>/role-padrao', methods=['POST'])
@login_required
@requer_permissao('cargos.editar')
def api_definir_role_padrao_cargo(cargo_id):
    """API: Define role padrão para um cargo"""
    cargo = Cargo.query.get_or_404(cargo_id)
    data = request.get_json()
    
    try:
        role_id = data.get('role_id')
        if role_id:
            role = Role.query.get(role_id)
            cargo.role_padrao = role
        else:
            cargo.role_padrao = None
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Role padrão definido com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@permissoes_bp.route('/api/departamento/<int:depto_id>/role-padrao', methods=['POST'])
@login_required
@requer_permissao('departamentos.editar')
def api_definir_role_padrao_departamento(depto_id):
    """API: Define role padrão para um departamento"""
    departamento = Departamento.query.get_or_404(depto_id)
    data = request.get_json()
    
    try:
        role_id = data.get('role_id')
        if role_id:
            role = Role.query.get(role_id)
            departamento.role_padrao = role
        else:
            departamento.role_padrao = None
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Role padrão definido com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
