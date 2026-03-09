from app import db
from datetime import datetime

class RegistroPonto(db.Model):
    """Modelo de Registro de Ponto"""
    __tablename__ = 'registro_ponto'
    
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    
    # Data e hora
    data = db.Column(db.Date, nullable=False, index=True)
    horario = db.Column(db.Time, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'entrada', 'saida', 'inicio_intervalo', 'fim_intervalo'
    
    # Localização GPS
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    localizacao_texto = db.Column(db.String(500))
    distancia_empresa = db.Column(db.Numeric(10, 2))  # em metros
    
    # Home Office
    home_office = db.Column(db.Boolean, default=False)
    home_office_autorizado = db.Column(db.Boolean, default=False)
    
    # Validações
    dentro_horario = db.Column(db.Boolean, default=True)
    atraso_minutos = db.Column(db.Integer, default=0)
    
    # Auditoria
    dispositivo = db.Column(db.String(200))
    ip_address = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    justificativa_atraso = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    colaborador = db.relationship('Colaborador', backref='registros_ponto')
    
    def __repr__(self):
        return f'<RegistroPonto {self.colaborador_id} - {self.data} {self.horario}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'colaborador_id': self.colaborador_id,
            'data': self.data.isoformat() if self.data else None,
            'horario': self.horario.strftime('%H:%M:%S') if self.horario else None,
            'tipo': self.tipo,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'localizacao_texto': self.localizacao_texto,
            'home_office': self.home_office,
            'home_office_autorizado': self.home_office_autorizado,
            'atraso_minutos': self.atraso_minutos
        }
