#!/usr/bin/env python3
"""
Cria Sistema de Níveis de Acesso e Permissões para RH
Integração com cadastro de colaboradores por cargo/departamento
"""

from pathlib import Path

def create_models_permissoes():
    """Cria models para sistema de permissões"""
    
    models_content = '''"""
Models para Sistema de Permissões e Níveis de Acesso
"""

from app import db
from datetime import datetime

# Tabela de associação muitos-para-muitos entre Roles e Permissões
role_permissoes = db.Table('role_permissoes',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permissao_id', db.Integer, db.ForeignKey('permissao.id'), primary_key=True),
    db.Column('data_criacao', db.DateTime, default=datetime.utcnow)
)

# Tabela de associação entre Usuários e Roles
usuario_roles = db.Table('usuario_roles',
    db.Column('usuario_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('data_atribuicao', db.DateTime, default=datetime.utcnow)
)

class Permissao(db.Model):
    """Permissões individuais do sistema"""
    __tablename__ = 'permissao'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # Ex: 'usuarios.criar'
    descricao = db.Column(db.Text)
    modulo = db.Column(db.String(50))  # Ex: 'rh', 'consultoria', 'projetos'
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    roles = db.relationship('Role', secondary=role_permissoes, back_populates='permissoes')
    
    def __repr__(self):
        return f'<Permissao {self.codigo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'modulo': self.modulo,
            'ativo': self.ativo
        }

class Role(db.Model):
    """Perfis/Papéis de acesso (Roles)"""
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # Ex: 'admin', 'gestor_rh'
    descricao = db.Column(db.Text)
    nivel_hierarquico = db.Column(db.Integer, default=0)  # 0=baixo, 10=alto
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    permissoes = db.relationship('Permissao', secondary=role_permissoes, back_populates='roles')
    usuarios = db.relationship('User', secondary=usuario_roles, back_populates='roles')
    cargos = db.relationship('Cargo', back_populates='role_padrao')
    departamentos = db.relationship('Departamento', back_populates='role_padrao')
    
    def __repr__(self):
        return f'<Role {self.nome}>'
    
    def tem_permissao(self, codigo_permissao):
        """Verifica se o role tem determinada permissão"""
        return any(p.codigo == codigo_permissao and p.ativo for p in self.permissoes)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'nivel_hierarquico': self.nivel_hierarquico,
            'ativo': self.ativo,
            'permissoes': [p.to_dict() for p in self.permissoes]
        }

class NivelAcesso(db.Model):
    """Níveis de acesso customizados por colaborador"""
    __tablename__ = 'nivel_acesso'
    
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    tipo_acesso = db.Column(db.String(50))  # 'completo', 'limitado', 'somente_leitura'
    modulos_liberados = db.Column(db.JSON)  # Lista de módulos: ['rh', 'consultoria', 'projetos']
    restricoes = db.Column(db.JSON)  # Restrições específicas
    ip_permitidos = db.Column(db.JSON)  # IPs permitidos (opcional)
    horario_acesso = db.Column(db.JSON)  # Horários permitidos (opcional)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)  # Acesso temporário (opcional)
    ativo = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    criado_por = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    colaborador = db.relationship('Colaborador', back_populates='nivel_acesso')
    criador = db.relationship('User', foreign_keys=[criado_por])
    
    def __repr__(self):
        return f'<NivelAcesso {self.colaborador_id} - {self.tipo_acesso}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tipo_acesso': self.tipo_acesso,
            'modulos_liberados': self.modulos_liberados,
            'restricoes': self.restricoes,
            'ativo': self.ativo,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None
        }

# Adicionar campos aos models existentes
class User(db.Model):
    # ... campos existentes ...
    
    # Novos relacionamentos
    roles = db.relationship('Role', secondary=usuario_roles, back_populates='usuarios')
    
    def tem_permissao(self, codigo_permissao):
        """Verifica se usuário tem determinada permissão através de seus roles"""
        return any(role.tem_permissao(codigo_permissao) for role in self.roles if role.ativo)
    
    def tem_role(self, codigo_role):
        """Verifica se usuário tem determinado role"""
        return any(role.codigo == codigo_role and role.ativo for role in self.roles)
    
    def get_permissoes(self):
        """Retorna todas as permissões do usuário"""
        permissoes = set()
        for role in self.roles:
            if role.ativo:
                permissoes.update([p.codigo for p in role.permissoes if p.ativo])
        return list(permissoes)

class Cargo(db.Model):
    # ... campos existentes ...
    
    # Novo campo
    role_padrao_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role_padrao = db.relationship('Role', back_populates='cargos')

class Departamento(db.Model):
    # ... campos existentes ...
    
    # Novo campo
    role_padrao_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role_padrao = db.relationship('Role', back_populates='departamentos')

class Colaborador(db.Model):
    # ... campos existentes ...
    
    # Novo relacionamento
    nivel_acesso = db.relationship('NivelAcesso', back_populates='colaborador', uselist=False)
'''
    
    return models_content

def create_permissoes_routes():
    """Cria rotas para gestão de permissões"""
    
    routes_content = '''"""
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
'''
    
    return routes_content

def create_permissoes_seed():
    """Cria script para popular permissões padrão"""
    
    seed_content = '''"""
Script para popular permissões e roles padrão do sistema
Execute: python seed_permissoes.py
"""

from app import create_app, db
from app.models import Permissao, Role

app = create_app()

def criar_permissoes_padrao():
    """Cria permissões padrão do sistema"""
    
    permissoes = [
        # Permissões de Usuários
        {'nome': 'Visualizar Usuários', 'codigo': 'usuarios.visualizar', 'modulo': 'usuarios'},
        {'nome': 'Criar Usuários', 'codigo': 'usuarios.criar', 'modulo': 'usuarios'},
        {'nome': 'Editar Usuários', 'codigo': 'usuarios.editar', 'modulo': 'usuarios'},
        {'nome': 'Excluir Usuários', 'codigo': 'usuarios.excluir', 'modulo': 'usuarios'},
        
        # Permissões de RH
        {'nome': 'Visualizar Colaboradores', 'codigo': 'colaboradores.visualizar', 'modulo': 'rh'},
        {'nome': 'Criar Colaboradores', 'codigo': 'colaboradores.criar', 'modulo': 'rh'},
        {'nome': 'Editar Colaboradores', 'codigo': 'colaboradores.editar', 'modulo': 'rh'},
        {'nome': 'Excluir Colaboradores', 'codigo': 'colaboradores.excluir', 'modulo': 'rh'},
        {'nome': 'Gerenciar Folha de Pagamento', 'codigo': 'folha.gerenciar', 'modulo': 'rh'},
        {'nome': 'Visualizar Relatórios RH', 'codigo': 'rh.relatorios', 'modulo': 'rh'},
        
        # Permissões de Consultoria
        {'nome': 'Visualizar Projetos Consultoria', 'codigo': 'consultoria.visualizar', 'modulo': 'consultoria'},
        {'nome': 'Criar Projetos Consultoria', 'codigo': 'consultoria.criar', 'modulo': 'consultoria'},
        {'nome': 'Editar Projetos Consultoria', 'codigo': 'consultoria.editar', 'modulo': 'consultoria'},
        {'nome': 'Realizar Diagnósticos', 'codigo': 'diagnosticos.realizar', 'modulo': 'consultoria'},
        {'nome': 'Gerenciar Auditorias', 'codigo': 'auditorias.gerenciar', 'modulo': 'consultoria'},
        
        # Permissões de Projetos
        {'nome': 'Visualizar Projetos', 'codigo': 'projetos.visualizar', 'modulo': 'projetos'},
        {'nome': 'Criar Projetos', 'codigo': 'projetos.criar', 'modulo': 'projetos'},
        {'nome': 'Editar Projetos', 'codigo': 'projetos.editar', 'modulo': 'projetos'},
        {'nome': 'Excluir Projetos', 'codigo': 'projetos.excluir', 'modulo': 'projetos'},
        
        # Permissões de Permissões/Roles
        {'nome': 'Visualizar Permissões', 'codigo': 'permissoes.visualizar', 'modulo': 'sistema'},
        {'nome': 'Gerenciar Permissões', 'codigo': 'permissoes.gerenciar', 'modulo': 'sistema'},
        {'nome': 'Visualizar Roles', 'codigo': 'roles.visualizar', 'modulo': 'sistema'},
        {'nome': 'Criar Roles', 'codigo': 'roles.criar', 'modulo': 'sistema'},
        {'nome': 'Editar Roles', 'codigo': 'roles.editar', 'modulo': 'sistema'},
        {'nome': 'Gerenciar Níveis de Acesso', 'codigo': 'nivel_acesso.gerenciar', 'modulo': 'sistema'},
        
        # Permissões de Configurações
        {'nome': 'Acessar Configurações', 'codigo': 'config.acessar', 'modulo': 'sistema'},
        {'nome': 'Gerenciar Cargos', 'codigo': 'cargos.editar', 'modulo': 'rh'},
        {'nome': 'Gerenciar Departamentos', 'codigo': 'departamentos.editar', 'modulo': 'rh'},
    ]
    
    print("Criando permissões padrão...")
    for perm_data in permissoes:
        perm = Permissao.query.filter_by(codigo=perm_data['codigo']).first()
        if not perm:
            perm = Permissao(**perm_data, descricao=f"Permissão para {perm_data['nome']}")
            db.session.add(perm)
            print(f"  ✓ Criada: {perm_data['nome']}")
        else:
            print(f"  - Já existe: {perm_data['nome']}")
    
    db.session.commit()
    print("✅ Permissões criadas!\n")

def criar_roles_padrao():
    """Cria roles padrão do sistema"""
    
    roles_config = [
        {
            'nome': 'Administrador',
            'codigo': 'admin',
            'descricao': 'Acesso total ao sistema',
            'nivel_hierarquico': 10,
            'permissoes': 'todas'  # Todas as permissões
        },
        {
            'nome': 'Gestor RH',
            'codigo': 'gestor_rh',
            'descricao': 'Gestão completa do módulo RH',
            'nivel_hierarquico': 8,
            'permissoes': [
                'colaboradores.visualizar', 'colaboradores.criar', 'colaboradores.editar',
                'folha.gerenciar', 'rh.relatorios', 'cargos.editar', 'departamentos.editar',
                'nivel_acesso.gerenciar'
            ]
        },
        {
            'nome': 'Analista RH',
            'codigo': 'analista_rh',
            'descricao': 'Operações de RH sem acesso à folha',
            'nivel_hierarquico': 5,
            'permissoes': [
                'colaboradores.visualizar', 'colaboradores.criar', 'colaboradores.editar',
                'rh.relatorios'
            ]
        },
        {
            'nome': 'Consultor',
            'codigo': 'consultor',
            'descricao': 'Acesso ao módulo de consultoria',
            'nivel_hierarquico': 6,
            'permissoes': [
                'consultoria.visualizar', 'consultoria.criar', 'consultoria.editar',
                'diagnosticos.realizar', 'auditorias.gerenciar'
            ]
        },
        {
            'nome': 'Gerente de Projetos',
            'codigo': 'gerente_projetos',
            'descricao': 'Gestão completa de projetos',
            'nivel_hierarquico': 7,
            'permissoes': [
                'projetos.visualizar', 'projetos.criar', 'projetos.editar', 'projetos.excluir'
            ]
        },
        {
            'nome': 'Colaborador',
            'codigo': 'colaborador',
            'descricao': 'Acesso básico ao sistema',
            'nivel_hierarquico': 1,
            'permissoes': [
                'colaboradores.visualizar'  # Apenas visualizar próprio perfil
            ]
        },
        {
            'nome': 'Auditor',
            'codigo': 'auditor',
            'descricao': 'Realiza auditorias e inspeções',
            'nivel_hierarquico': 6,
            'permissoes': [
                'auditorias.gerenciar', 'consultoria.visualizar', 'diagnosticos.realizar'
            ]
        }
    ]
    
    print("Criando roles padrão...")
    for role_data in roles_config:
        role = Role.query.filter_by(codigo=role_data['codigo']).first()
        
        if not role:
            role = Role(
                nome=role_data['nome'],
                codigo=role_data['codigo'],
                descricao=role_data['descricao'],
                nivel_hierarquico=role_data['nivel_hierarquico']
            )
            db.session.add(role)
            db.session.flush()
            
            # Atribuir permissões
            if role_data['permissoes'] == 'todas':
                permissoes = Permissao.query.all()
            else:
                permissoes = Permissao.query.filter(Permissao.codigo.in_(role_data['permissoes'])).all()
            
            role.permissoes = permissoes
            print(f"  ✓ Criado: {role_data['nome']} com {len(permissoes)} permissões")
        else:
            print(f"  - Já existe: {role_data['nome']}")
    
    db.session.commit()
    print("✅ Roles criados!\n")

def main():
    """Executa seed de permissões"""
    with app.app_context():
        print("="*60)
        print("POPULANDO PERMISSÕES E ROLES DO SISTEMA")
        print("="*60 + "\n")
        
        criar_permissoes_padrao()
        criar_roles_padrao()
        
        print("="*60)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print("="*60)
        
        # Estatísticas
        total_permissoes = Permissao.query.count()
        total_roles = Role.query.count()
        
        print(f"\n📊 Estatísticas:")
        print(f"   • Permissões: {total_permissoes}")
        print(f"   • Roles: {total_roles}")

if __name__ == '__main__':
    main()
'''
    
    return seed_content

def create_permissoes_template():
    """Cria template para página de gestão de permissões"""
    
    template_content = '''{% extends "base.html" %}

{% block title %}Gestão de Permissões - RH{% endblock %}

{% block content %}
<div class="container-fluid">
    <!-- Header -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">
            <i class="fas fa-shield-alt me-2"></i>Gestão de Permissões e Níveis de Acesso
        </h1>
        <div class="btn-group">
            <button class="btn btn-success" onclick="novoRole()">
                <i class="fas fa-plus me-1"></i>Novo Role
            </button>
            <button class="btn btn-outline-primary" onclick="exportarPermissoes()">
                <i class="fas fa-file-export me-1"></i>Exportar
            </button>
            <a href="{{ url_for('rh.index') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left me-1"></i>Voltar
            </a>
        </div>
    </div>

    <!-- Info -->
    <div class="alert alert-info alert-dismissible fade show">
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        <h5 class="alert-heading">
            <i class="fas fa-info-circle me-2"></i>Sistema de Controle de Acesso
        </h5>
        <p class="mb-0">
            Gerencie <strong>Roles (Perfis)</strong>, <strong>Permissões</strong> e 
            <strong>Níveis de Acesso</strong> por colaborador, cargo ou departamento.
            Sistema hierárquico com controle granular de funcionalidades.
        </p>
    </div>

    <!-- Tabs -->
    <ul class="nav nav-tabs mb-4" id="permissoesTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active" id="roles-tab" data-bs-toggle="tab" data-bs-target="#roles" type="button">
                <i class="fas fa-user-shield me-1"></i>Roles (Perfis)
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="permissoes-tab" data-bs-toggle="tab" data-bs-target="#permissoes" type="button">
                <i class="fas fa-key me-1"></i>Permissões
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="cargos-tab" data-bs-toggle="tab" data-bs-target="#cargos" type="button">
                <i class="fas fa-briefcase me-1"></i>Cargos
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="departamentos-tab" data-bs-toggle="tab" data-bs-target="#departamentos" type="button">
                <i class="fas fa-building me-1"></i>Departamentos
            </button>
        </li>
    </ul>

    <!-- Tab Content -->
    <div class="tab-content" id="permissoesTabContent">
        <!-- Tab Roles -->
        <div class="tab-pane fade show active" id="roles" role="tabpanel">
            <div class="card shadow">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">
                        <i class="fas fa-user-shield me-2"></i>Roles (Perfis de Acesso)
                    </h6>
                </div>
                <div class="card-body">
                    <div id="listaRoles">
                        <!-- Preenchido dinamicamente -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab Permissões -->
        <div class="tab-pane fade" id="permissoes" role="tabpanel">
            <div class="card shadow">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">
                        <i class="fas fa-key me-2"></i>Permissões do Sistema
                    </h6>
                </div>
                <div class="card-body">
                    <div id="listaPermissoes">
                        <!-- Preenchido dinamicamente -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab Cargos -->
        <div class="tab-pane fade" id="cargos" role="tabpanel">
            <div class="card shadow">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">
                        <i class="fas fa-briefcase me-2"></i>Roles Padrão por Cargo
                    </h6>
                </div>
                <div class="card-body">
                    <p class="text-muted">
                        Defina qual role será atribuído automaticamente ao criar colaborador com determinado cargo.
                    </p>
                    <div id="listaCargosRoles">
                        <!-- Preenchido dinamicamente -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab Departamentos -->
        <div class="tab-pane fade" id="departamentos" role="tabpanel">
            <div class="card shadow">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">
                        <i class="fas fa-building me-2"></i>Roles Padrão por Departamento
                    </h6>
                </div>
                <div class="card-body">
                    <p class="text-muted">
                        Defina qual role será atribuído automaticamente ao criar colaborador em determinado departamento.
                    </p>
                    <div id="listaDepartamentosRoles">
                        <!-- Preenchido dinamicamente -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal Novo/Editar Role -->
<div class="modal fade" id="modalRole" tabindex="-1">
    <div class="modal-dialog modal-xl">
        <div class="modal-content">
            <div class="modal-header bg-primary text-white">
                <h5 class="modal-title">
                    <i class="fas fa-user-shield me-2"></i><span id="tituloModalRole">Novo Role</span>
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <form id="formRole">
                    <div class="row">
                        <div class="col-md-6">
                            <label class="form-label"><strong>Nome do Role*</strong></label>
                            <input type="text" class="form-control" id="nomeRole" required
                                placeholder="Ex: Gerente de RH">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label"><strong>Código*</strong></label>
                            <input type="text" class="form-control" id="codigoRole" required
                                placeholder="Ex: gerente_rh">
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col-md-9">
                            <label class="form-label"><strong>Descrição</strong></label>
                            <input type="text" class="form-control" id="descricaoRole"
                                placeholder="Breve descrição do perfil">
                        </div>
                        <div class="col-md-3">
                            <label class="form-label"><strong>Nível Hierárquico*</strong></label>
                            <input type="number" class="form-control" id="nivelRole" value="5" min="0" max="10">
                            <small class="text-muted">0=baixo, 10=alto</small>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-12">
                            <h6 class="border-bottom pb-2">Permissões</h6>
                            <div id="permissoesCheckboxes">
                                <!-- Preenchido dinamicamente -->
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="button" class="btn btn-success" onclick="salvarRole()">
                    <i class="fas fa-save me-1"></i>Salvar Role
                </button>
            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block scripts %}
<script>
// ===== DADOS E FUNÇÕES =====

let roles = [];
let permissoes = {};

function carregarRoles() {
    fetch('/rh/permissoes/api/roles')
        .then(r => r.json())
        .then(data => {
            roles = data.roles;
            renderizarRoles();
        });
}

function carregarPermissoes() {
    fetch('/rh/permissoes/api/permissoes')
        .then(r => r.json())
        .then(data => {
            permissoes = data.permissoes;
            renderizarPermissoes();
        });
}

function renderizarRoles() {
    const container = document.getElementById('listaRoles');
    container.innerHTML = '';
    
    roles.forEach(role => {
        const nivelColor = role.nivel_hierarquico >= 8 ? 'danger' : 
                          role.nivel_hierarquico >= 5 ? 'warning' : 'info';
        
        const card = `
            <div class="card mb-3">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-6">
                            <h5 class="mb-1">
                                <i class="fas fa-user-shield text-primary me-2"></i>
                                ${role.nome}
                            </h5>
                            <p class="text-muted mb-0">${role.descricao || 'Sem descrição'}</p>
                            <small class="text-muted">Código: <code>${role.codigo}</code></small>
                        </div>
                        <div class="col-md-3">
                            <span class="badge bg-${nivelColor} me-2">Nível ${role.nivel_hierarquico}</span>
                            <span class="badge bg-secondary">${role.permissoes.length} permissões</span>
                        </div>
                        <div class="col-md-3 text-end">
                            <button class="btn btn-sm btn-primary" onclick="editarRole(${role.id})">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="btn btn-sm btn-info" onclick="verPermissoesRole(${role.id})">
                                <i class="fas fa-key"></i> Permissões
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}

function renderizarPermissoes() {
    const container = document.getElementById('listaPermissoes');
    container.innerHTML = '';
    
    for (const [modulo, perms] of Object.entries(permissoes)) {
        let html = `
            <div class="card mb-3">
                <div class="card-header">
                    <h6 class="mb-0 text-capitalize">
                        <i class="fas fa-cube me-2"></i>Módulo: ${modulo}
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row">
        `;
        
        perms.forEach(perm => {
            html += `
                <div class="col-md-4 mb-2">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" disabled checked>
                        <label class="form-check-label">
                            <strong>${perm.nome}</strong><br>
                            <small class="text-muted"><code>${perm.codigo}</code></small>
                        </label>
                    </div>
                </div>
            `;
        });
        
        html += `
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML += html;
    }
}

function novoRole() {
    document.getElementById('tituloModalRole').textContent = 'Novo Role';
    document.getElementById('formRole').reset();
    carregarPermissoesCheckboxes();
    new bootstrap.Modal(document.getElementById('modalRole')).show();
}

function carregarPermissoesCheckboxes() {
    const container = document.getElementById('permissoesCheckboxes');
    container.innerHTML = '';
    
    for (const [modulo, perms] of Object.entries(permissoes)) {
        let html = `
            <div class="mb-3">
                <h6 class="text-capitalize">
                    <i class="fas fa-cube me-2"></i>${modulo}
                    <button class="btn btn-sm btn-outline-primary ms-2" onclick="selecionarTodosModulo('${modulo}')">
                        Selecionar Todos
                    </button>
                </h6>
                <div class="row">
        `;
        
        perms.forEach(perm => {
            html += `
                <div class="col-md-4 mb-2">
                    <div class="form-check">
                        <input class="form-check-input permissao-check" type="checkbox" 
                               value="${perm.id}" id="perm_${perm.id}" data-modulo="${modulo}">
                        <label class="form-check-label" for="perm_${perm.id}">
                            ${perm.nome}
                        </label>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
        
        container.innerHTML += html;
    }
}

function selecionarTodosModulo(modulo) {
    document.querySelectorAll(`.permissao-check[data-modulo="${modulo}"]`).forEach(cb => {
        cb.checked = true;
    });
}

function salvarRole() {
    const form = document.getElementById('formRole');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const permissoesSelecionadas = Array.from(document.querySelectorAll('.permissao-check:checked'))
        .map(cb => parseInt(cb.value));
    
    const dados = {
        nome: document.getElementById('nomeRole').value,
        codigo: document.getElementById('codigoRole').value,
        descricao: document.getElementById('descricaoRole').value,
        nivel_hierarquico: parseInt(document.getElementById('nivelRole').value),
        permissoes_ids: permissoesSelecionadas
    };
    
    fetch('/rh/permissoes/api/roles', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(dados)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Role criado com sucesso!');
            bootstrap.Modal.getInstance(document.getElementById('modalRole')).hide();
            carregarRoles();
        } else {
            alert('Erro: ' + data.message);
        }
    });
}

function editarRole(id) {
    alert('Editar role ' + id);
}

function verPermissoesRole(id) {
    alert('Ver permissões do role ' + id);
}

function exportarPermissoes() {
    alert('Exportar configuração de permissões');
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    carregarRoles();
    carregarPermissoes();
});
</script>
{% endblock %}'''
    
    return template_content

def create_nivel_acesso_template():
    """Cria template para configurar nível de acesso de colaborador"""
    
    template_content = '''{% extends "base.html" %}

{% block title %}Nível de Acesso - {{ colaborador.nome }}{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">
            <i class="fas fa-user-lock me-2"></i>Configurar Nível de Acesso
        </h1>
        <a href="{{ url_for('rh.colaboradores') }}" class="btn btn-secondary">
            <i class="fas fa-arrow-left me-1"></i>Voltar
        </a>
    </div>

    <!-- Info do Colaborador -->
    <div class="card shadow mb-4">
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <h5>{{ colaborador.nome }}</h5>
                    <p class="text-muted mb-0">
                        <strong>Cargo:</strong> {{ colaborador.cargo.nome if colaborador.cargo else 'Não definido' }} |
                        <strong>Departamento:</strong> {{ colaborador.departamento.nome if colaborador.departamento else 'Não definido' }}
                    </p>
                </div>
                <div class="col-md-4 text-end">
                    <span class="badge bg-primary fs-6">ID: {{ colaborador.id }}</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Formulário de Configuração -->
    <div class="card shadow">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">
                <i class="fas fa-cog me-2"></i>Configuração de Acesso
            </h6>
        </div>
        <div class="card-body">
            <form id="formNivelAcesso">
                <div class="row">
                    <div class="col-md-4">
                        <label class="form-label"><strong>Tipo de Acesso*</strong></label>
                        <select class="form-select" id="tipoAcesso" required>
                            <option value="completo">Acesso Completo</option>
                            <option value="limitado" selected>Acesso Limitado</option>
                            <option value="somente_leitura">Somente Leitura</option>
                        </select>
                    </div>
                    <div class="col-md-4">
                        <label class="form-label"><strong>Válido Até</strong></label>
                        <input type="date" class="form-control" id="dataFim">
                        <small class="text-muted">Deixe vazio para acesso permanente</small>
                    </div>
                    <div class="col-md-4">
                        <label class="form-label"><strong>Status</strong></label>
                        <select class="form-select" id="statusAcesso">
                            <option value="true" selected>Ativo</option>
                            <option value="false">Inativo</option>
                        </select>
                    </div>
                </div>

                <div class="row mt-4">
                    <div class="col-12">
                        <h6 class="border-bottom pb-2">Roles (Perfis de Acesso)</h6>
                        <div id="rolesCheckboxes">
                            <!-- Preenchido dinamicamente -->
                        </div>
                    </div>
                </div>

                <div class="row mt-4">
                    <div class="col-12">
                        <h6 class="border-bottom pb-2">Módulos Liberados</h6>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="form-check">
                                    <input class="form-check-input modulo-check" type="checkbox" value="rh" id="mod_rh">
                                    <label class="form-check-label" for="mod_rh">
                                        <i class="fas fa-users me-1"></i>Recursos Humanos
                                    </label>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-check">
                                    <input class="form-check-input modulo-check" type="checkbox" value="consultoria" id="mod_consultoria">
                                    <label class="form-check-label" for="mod_consultoria">
                                        <i class="fas fa-briefcase me-1"></i>Consultoria
                                    </label>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-check">
                                    <input class="form-check-input modulo-check" type="checkbox" value="projetos" id="mod_projetos">
                                    <label class="form-check-label" for="mod_projetos">
                                        <i class="fas fa-project-diagram me-1"></i>Projetos
                                    </label>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="form-check">
                                    <input class="form-check-input modulo-check" type="checkbox" value="relatorios" id="mod_relatorios">
                                    <label class="form-check-label" for="mod_relatorios">
                                        <i class="fas fa-chart-line me-1"></i>Relatórios
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row mt-4">
                    <div class="col-12">
                        <label class="form-label"><strong>Observações</strong></label>
                        <textarea class="form-control" id="observacoes" rows="3"
                            placeholder="Observações sobre o nível de acesso deste colaborador..."></textarea>
                    </div>
                </div>

                <div class="row mt-4">
                    <div class="col-12 text-end">
                        <button type="button" class="btn btn-secondary" onclick="history.back()">Cancelar</button>
                        <button type="button" class="btn btn-success" onclick="salvarNivelAcesso()">
                            <i class="fas fa-save me-1"></i>Salvar Configuração
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>

{% endblock %}

{% block scripts %}
<script>
const colaboradorId = {{ colaborador.id }};

function carregarRoles() {
    fetch('/rh/permissoes/api/roles')
        .then(r => r.json())
        .then(data => {
            renderizarRolesCheckboxes(data.roles);
        });
}

function renderizarRolesCheckboxes(roles) {
    const container = document.getElementById('rolesCheckboxes');
    container.innerHTML = '<div class="row">';
    
    roles.forEach(role => {
        const html = `
            <div class="col-md-4 mb-2">
                <div class="form-check">
                    <input class="form-check-input role-check" type="checkbox" value="${role.id}" id="role_${role.id}">
                    <label class="form-check-label" for="role_${role.id}">
                        <strong>${role.nome}</strong><br>
                        <small class="text-muted">${role.descricao || ''}</small>
                    </label>
                </div>
            </div>
        `;
        container.innerHTML += html;
    });
    
    container.innerHTML += '</div>';
}

function carregarNivelAcessoExistente() {
    fetch(`/rh/permissoes/api/nivel-acesso/${colaboradorId}`)
        .then(r => r.json())
        .then(data => {
            if (data.nivel_acesso) {
                // Preencher formulário com dados existentes
                const nivel = data.nivel_acesso;
                document.getElementById('tipoAcesso').value = nivel.tipo_acesso || 'limitado';
                document.getElementById('statusAcesso').value = nivel.ativo ? 'true' : 'false';
                
                if (nivel.modulos_liberados) {
                    nivel.modulos_liberados.forEach(mod => {
                        const checkbox = document.getElementById(`mod_${mod}`);
                        if (checkbox) checkbox.checked = true;
                    });
                }
            }
        });
}

function salvarNivelAcesso() {
    const rolesIds = Array.from(document.querySelectorAll('.role-check:checked')).map(cb => parseInt(cb.value));
    const modulosLiberados = Array.from(document.querySelectorAll('.modulo-check:checked')).map(cb => cb.value);
    
    const dados = {
        tipo_acesso: document.getElementById('tipoAcesso').value,
        modulos_liberados: modulosLiberados,
        data_fim: document.getElementById('dataFim').value || null,
        ativo: document.getElementById('statusAcesso').value === 'true',
        observacoes: document.getElementById('observacoes').value,
        roles_ids: rolesIds
    };
    
    fetch(`/rh/permissoes/api/nivel-acesso/${colaboradorId}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(dados)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Nível de acesso configurado com sucesso!');
            window.location.href = '/rh/colaboradores';
        } else {
            alert('Erro: ' + data.message);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    carregarRoles();
    carregarNivelAcessoExistente();
});
</script>
{% endblock %}'''
    
    return template_content

def main():
    """Cria sistema completo de permissões"""
    
    print("🚀 CRIANDO SISTEMA DE PERMISSÕES E NÍVEIS DE ACESSO")
    print("="*60)
    
    try:
        # Criar diretórios
        print("\n1. 📁 Criando estrutura de diretórios...")
        templates_dir = Path("app/templates/rh/permissoes")
        templates_dir.mkdir(parents=True, exist_ok=True)
        print("   ✅ Diretórios criados!")
        
        # Criar models
        print("\n2. 🗄️  Criando models...")
        models_content = create_models_permissoes()
        models_file = Path("app/models_permissoes.py")
        with open(models_file, 'w', encoding='utf-8') as f:
            f.write(models_content)
        print("   ✅ Models criados!")
        
        # Criar rotas
        print("\n3. 🛣️  Criando rotas...")
        routes_content = create_permissoes_routes()
        routes_file = Path("app/permissoes_routes.py")
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(routes_content)
        print("   ✅ Rotas criadas!")
        
        # Criar seed
        print("\n4. 🌱 Criando script de seed...")
        seed_content = create_permissoes_seed()
        seed_file = Path("seed_permissoes.py")
        with open(seed_file, 'w', encoding='utf-8') as f:
            f.write(seed_content)
        print("   ✅ Seed criado!")
        
        # Criar templates
        print("\n5. 📄 Criando templates...")
        
        # Template principal
        perm_template = create_permissoes_template()
        with open(templates_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(perm_template)
        print("   ✅ Template de permissões criado!")
        
        # Template nível de acesso
        nivel_template = create_nivel_acesso_template()
        with open(templates_dir / 'nivel_acesso.html', 'w', encoding='utf-8') as f:
            f.write(nivel_template)
        print("   ✅ Template de nível de acesso criado!")
        
        print(f"\n{'='*60}")
        print("✅ SISTEMA DE PERMISSÕES CRIADO COM SUCESSO!")
        
        print("\n📋 Componentes criados:")
        print("   ✅ Models (Permissao, Role, NivelAcesso)")
        print("   ✅ Rotas e APIs REST")
        print("   ✅ Templates HTML")
        print("   ✅ Script de seed")
        print("   ✅ Decorators de verificação")
        
        print("\n🎯 Funcionalidades:")
        print("   • Gestão de Roles (Perfis)")
        print("   • Gestão de Permissões")
        print("   • Níveis de acesso por colaborador")
        print("   • Roles padrão por cargo")
        print("   • Roles padrão por departamento")
        print("   • Sistema hierárquico")
        print("   • Controle granular de acesso")
        
        print("\n📊 7 Roles padrão:")
        print("   1. Administrador (nível 10)")
        print("   2. Gestor RH (nível 8)")
        print("   3. Analista RH (nível 5)")
        print("   4. Consultor (nível 6)")
        print("   5. Gerente de Projetos (nível 7)")
        print("   6. Colaborador (nível 1)")
        print("   7. Auditor (nível 6)")
        
        print("\n🔑 25+ Permissões distribuídas em:")
        print("   • Usuários")
        print("   • RH")
        print("   • Consultoria")
        print("   • Projetos")
        print("   • Sistema")
        
        print("\n🚀 Próximos passos:")
        print("   1. Adicione os models ao __init__.py:")
        print("      from app.models_permissoes import Role, Permissao, NivelAcesso")
        print("\n   2. Registre o blueprint:")
        print("      from app.permissoes_routes import permissoes_bp")
        print("      app.register_blueprint(permissoes_bp)")
        print("\n   3. Execute as migrações:")
        print("      flask db migrate -m 'Add permissoes system'")
        print("      flask db upgrade")
        print("\n   4. Popule os dados padrão:")
        print("      python seed_permissoes.py")
        print("\n   5. Acesse /rh/permissoes")
        
        print("\n💡 Integração com cadastro de colaborador:")
        print("   • Ao criar colaborador, atribuir role baseado em cargo/departamento")
        print("   • Link 'Configurar Acesso' na lista de colaboradores")
        print("   • Modal de nível de acesso no formulário de cadastro")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🎉 SISTEMA DE PERMISSÕES COMPLETO!")
    else:
        print(f"\n💥 ERRO NA CRIAÇÃO")