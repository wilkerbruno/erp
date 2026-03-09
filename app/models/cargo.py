from app import db
from datetime import datetime

class Cargo(db.Model):
    """Modelo de Cargo"""
    __tablename__ = 'cargo'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    nivel_hierarquico = db.Column(db.Integer, default=1)  # 1=operacional, 2=tático, 3=estratégico
    salario_base_min = db.Column(db.Numeric(10, 2))
    salario_base_max = db.Column(db.Numeric(10, 2))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos (serão criados quando Colaborador existir)
    # colaboradores = db.relationship('Colaborador', back_populates='cargo')
    
    def __repr__(self):
        return f'<Cargo {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'nivel_hierarquico': self.nivel_hierarquico,
            'salario_base_min': float(self.salario_base_min) if self.salario_base_min else None,
            'salario_base_max': float(self.salario_base_max) if self.salario_base_max else None,
            'ativo': self.ativo
        }
