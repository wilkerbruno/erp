from app import db
from datetime import datetime

class Beneficio(db.Model):
    """Modelo de Benefício"""
    __tablename__ = 'beneficio'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(20))  # 'fixo', 'variavel', 'percentual'
    
    # Valor
    valor_fixo = db.Column(db.Numeric(10, 2))
    percentual = db.Column(db.Numeric(5, 2))
    
    # Condições
    requer_desempenho = db.Column(db.Boolean, default=False)
    meta_minima = db.Column(db.Numeric(10, 2))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Beneficio {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'valor_fixo': float(self.valor_fixo) if self.valor_fixo else None,
            'percentual': float(self.percentual) if self.percentual else None,
            'ativo': self.ativo
        }


class ColaboradorBeneficio(db.Model):
    """Relacionamento entre Colaborador e Benefício"""
    __tablename__ = 'colaborador_beneficio'
    
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    beneficio_id = db.Column(db.Integer, db.ForeignKey('beneficio.id'), nullable=False)
    
    # Valor customizado (sobrescreve o valor padrão do benefício)
    valor_customizado = db.Column(db.Numeric(10, 2))
    
    # Período
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date)
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    colaborador = db.relationship('Colaborador', backref='beneficios')
    beneficio = db.relationship('Beneficio', backref='colaboradores')
    
    def __repr__(self):
        return f'<ColaboradorBeneficio {self.colaborador_id}-{self.beneficio_id}>'


class CargoBeneficio(db.Model):
    """Benefícios padrão por cargo"""
    __tablename__ = 'cargo_beneficio'
    
    id = db.Column(db.Integer, primary_key=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'), nullable=False)
    beneficio_id = db.Column(db.Integer, db.ForeignKey('beneficio.id'), nullable=False)
    
    # Valor padrão para este cargo
    valor_padrao = db.Column(db.Numeric(10, 2))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    cargo = db.relationship('Cargo', backref='beneficios_padrao')
    beneficio = db.relationship('Beneficio', backref='cargos')
    
    def __repr__(self):
        return f'<CargoBeneficio {self.cargo_id}-{self.beneficio_id}>'
