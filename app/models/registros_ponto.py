# ====================================================================
# MODELOS ADAPTADOS ÀS SUAS TABELAS EXISTENTES
# Cole este código em: app/models.py (se não existir o modelo ainda)
# ====================================================================

from app import db
from datetime import datetime

class RegistroPonto(db.Model):
    """Modelo para registro de ponto - ADAPTADO À SUA TABELA EXISTENTE"""
    __tablename__ = 'registros_ponto'
    
    # Campos da sua tabela
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data = db.Column(db.Date, nullable=False, index=True)
    horario = db.Column(db.Time, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    
    # Localização
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    localizacao_texto = db.Column(db.String(500))
    
    # Home office
    home_office = db.Column(db.Boolean, default=False)
    home_office_autorizado = db.Column(db.Boolean, default=False)
    
    # Controle de atraso
    atraso_minutos = db.Column(db.Integer, default=0)
    justificativa_atraso = db.Column(db.String(500))
    
    # Dispositivo e IP
    dispositivo = db.Column(db.String(500))
    ip_address = db.Column(db.String(50))
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    colaborador = db.relationship('User', backref='registros_ponto', lazy=True)
    
    def __repr__(self):
        return f'<RegistroPonto {self.colaborador_id} - {self.data} {self.horario} - {self.tipo}>'
    
    def to_dict(self):
        """Converte o registro para dicionário"""
        return {
            'id': self.id,
            'colaborador_id': self.colaborador_id,
            'data': self.data.strftime('%Y-%m-%d') if self.data else None,
            'horario': self.horario.strftime('%H:%M:%S') if self.horario else None,
            'tipo': self.tipo,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'localizacao_texto': self.localizacao_texto,
            'home_office': self.home_office,
            'home_office_autorizado': self.home_office_autorizado,
            'atraso_minutos': self.atraso_minutos,
            'dentro_horario': self.atraso_minutos == 0,
            'justificativa_atraso': self.justificativa_atraso,
            'dispositivo': self.dispositivo,
            'ip_address': self.ip_address,
            'criado_em': self.criado_em.strftime('%Y-%m-%d %H:%M:%S') if self.criado_em else None
        }


class AutorizacaoHomeOffice(db.Model):
    """Modelo para autorização de home office - ADAPTADO À SUA TABELA"""
    __tablename__ = 'autorizacoes_home_office'
    
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    autorizado_por = db.Column(db.Integer, db.ForeignKey('users.id'))
    observacoes = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    colaborador = db.relationship('User', foreign_keys=[colaborador_id], backref='autorizacoes_home_office')
    autorizador = db.relationship('User', foreign_keys=[autorizado_por])
    
    def __repr__(self):
        return f'<AutorizacaoHomeOffice {self.colaborador_id} - {self.data_inicio} a {self.data_fim}>'
    
    @staticmethod
    def verificar_autorizacao(colaborador_id, data):
        """Verifica se há autorização de home office para a data"""
        from datetime import datetime
        if isinstance(data, str):
            data = datetime.strptime(data, '%Y-%m-%d').date()
        
        autorizacao = AutorizacaoHomeOffice.query.filter(
            AutorizacaoHomeOffice.colaborador_id == colaborador_id,
            AutorizacaoHomeOffice.data_inicio <= data,
            AutorizacaoHomeOffice.data_fim >= data,
            AutorizacaoHomeOffice.ativo == True
        ).first()
        
        return autorizacao is not None