from app import db
from datetime import datetime

class AutorizacaoHomeOffice(db.Model):
    """Modelo de Autorização de Home Office"""
    __tablename__ = 'autorizacao_home_office'
    
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    
    # Período
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date)  # Null = indefinido
    
    # Dias da semana permitidos
    dias_semana = db.Column(db.JSON)  # ['segunda', 'quarta', 'sexta']
    
    # Autorização
    autorizado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    motivo = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(20), default='ativo')  # 'ativo', 'expirado', 'cancelado'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    colaborador = db.relationship('Colaborador', backref='autorizacoes_homeoffice')
    autorizador = db.relationship('User', foreign_keys=[autorizado_por])
    
    def __repr__(self):
        return f'<AutorizacaoHomeOffice {self.colaborador_id} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'colaborador_id': self.colaborador_id,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'dias_semana': self.dias_semana,
            'motivo': self.motivo,
            'status': self.status
        }


class AuxilioCelular(db.Model):
    """Modelo de Auxílio Celular"""
    __tablename__ = 'auxilio_celular'
    
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    
    # Valor
    valor_mensal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Período
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date)
    
    # Justificativa
    motivo_concessao = db.Column(db.Text)
    
    # Autorização
    criado_por = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    colaborador = db.relationship('Colaborador', backref='auxilios_celular')
    criador = db.relationship('User', foreign_keys=[criado_por])
    
    def __repr__(self):
        return f'<AuxilioCelular {self.colaborador_id} - R$ {self.valor_mensal}>'
