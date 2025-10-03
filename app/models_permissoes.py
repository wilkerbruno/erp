"""
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
