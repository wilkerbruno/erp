from app import db
from datetime import datetime

class Departamento(db.Model):
    """Modelo de Departamento"""
    __tablename__ = 'departamento'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    sigla = db.Column(db.String(10))
    descricao = db.Column(db.Text)
    
    # Gestor do departamento
    gestor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Centro de custo
    centro_custo_codigo = db.Column(db.String(20))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    gestor = db.relationship('User', foreign_keys=[gestor_id])
    # colaboradores = db.relationship('Colaborador', back_populates='departamento')
    
    def __repr__(self):
        return f'<Departamento {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sigla': self.sigla,
            'descricao': self.descricao,
            'gestor_id': self.gestor_id,
            'centro_custo_codigo': self.centro_custo_codigo,
            'ativo': self.ativo
        }
