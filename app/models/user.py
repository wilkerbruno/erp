from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # Campos básicos
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    perfil = db.Column(db.String(20), default='user')  # user, gestor, admin
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    # Removendo login_count que estava causando problema
    
    def set_password(self, password):
        """Define a senha do usuário"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        # Admin tem acesso a tudo
        if self.perfil == 'admin':
            return True
        
        # Gestor tem acesso a quase tudo, exceto configurações
        if self.perfil == 'gestor':
            restricted = ['admin', 'configuracoes']
            return permission not in restricted
        
        # Usuário comum tem acesso limitado
        if self.perfil == 'user':
            allowed = ['dashboard', 'planos_acao', 'relatorios']
            return permission in allowed
        
        return False
    
    def is_admin(self):
        """Verifica se é administrador"""
        return self.perfil == 'admin'
    
    def is_gestor(self):
        """Verifica se é gestor"""
        return self.perfil in ['admin', 'gestor']
    
    def get_display_name(self):
        """Retorna o nome para exibição"""
        return self.username.title()
    
    def get_perfil_display(self):
        """Retorna o perfil formatado para exibição"""
        perfis = {
            'admin': 'Administrador',
            'gestor': 'Gestor',
            'user': 'Usuário'
        }
        return perfis.get(self.perfil, 'Usuário')
    
    def __repr__(self):
        return f'<User {self.username}>'