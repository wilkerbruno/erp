# ====================================================================
# MODELOS ADAPTADOS ÀS SUAS TABELAS EXISTENTES
# Cole este código em: app/models.py (se não existir o modelo ainda)
# ====================================================================

from app import db
from datetime import datetime

class RegistroPonto(db.Model):
    """Modelo para registro de ponto - COM CÁLCULO DE HORAS"""
    __tablename__ = 'registros_ponto'
    
    # Campos básicos
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
    
    # ✅ NOVA COLUNA: Total de horas trabalhadas
    total_horas = db.Column(db.Numeric(5, 2), default=0.00)
    
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
            'total_horas': float(self.total_horas) if self.total_horas else 0.0,
            'criado_em': self.criado_em.strftime('%Y-%m-%d %H:%M:%S') if self.criado_em else None
        }
    
    @staticmethod
    def calcular_horas_trabalhadas(colaborador_id, data):
        """
        Calcula o total de horas trabalhadas em um dia
        
        Lógica:
        - Período manhã: entrada até saida_almoco
        - Período tarde: volta_almoco até saida
        - Total: soma dos dois períodos
        
        Retorna: total de horas em decimal (ex: 8.5 horas)
        """
        from datetime import datetime, timedelta
        
        # Buscar todos os registros do dia
        registros = RegistroPonto.query.filter(
            RegistroPonto.colaborador_id == colaborador_id,
            RegistroPonto.data == data
        ).order_by(RegistroPonto.horario.asc()).all()
        
        if not registros:
            return 0.0
        
        # Organizar registros por tipo
        pontos = {}
        for r in registros:
            pontos[r.tipo] = r.horario
        
        total_horas = 0.0
        
        try:
            # Período manhã: entrada até saida_almoco
            if 'entrada' in pontos and 'saida_almoco' in pontos:
                entrada = pontos['entrada']
                saida_almoco = pontos['saida_almoco']
                
                # Converter Time para datetime para calcular diferença
                dt_entrada = datetime.combine(data, entrada)
                dt_saida_almoco = datetime.combine(data, saida_almoco)
                
                # Calcular diferença
                delta_manha = dt_saida_almoco - dt_entrada
                horas_manha = delta_manha.total_seconds() / 3600.0
                total_horas += horas_manha
            
            # Período tarde: volta_almoco até saida
            if 'volta_almoco' in pontos and 'saida' in pontos:
                volta_almoco = pontos['volta_almoco']
                saida = pontos['saida']
                
                # Converter Time para datetime
                dt_volta_almoco = datetime.combine(data, volta_almoco)
                dt_saida = datetime.combine(data, saida)
                
                # Calcular diferença
                delta_tarde = dt_saida - dt_volta_almoco
                horas_tarde = delta_tarde.total_seconds() / 3600.0
                total_horas += horas_tarde
        
        except Exception as e:
            print(f"⚠️ Erro ao calcular horas: {e}")
            return 0.0
        
        return round(total_horas, 2)
    
    @staticmethod
    def atualizar_total_horas(colaborador_id, data):
        """
        Atualiza o campo total_horas para todos os registros do dia
        
        Deve ser chamado sempre que um registro é adicionado/alterado
        """
        from app import db
        
        # Calcular total de horas
        total = RegistroPonto.calcular_horas_trabalhadas(colaborador_id, data)
        
        # Atualizar todos os registros do dia
        RegistroPonto.query.filter(
            RegistroPonto.colaborador_id == colaborador_id,
            RegistroPonto.data == data
        ).update({'total_horas': total})
        
        db.session.commit()
        
        return total
    
    @staticmethod
    def obter_resumo_dia(colaborador_id, data):
        """
        Retorna um resumo do dia com todos os pontos e total de horas
        """
        registros = RegistroPonto.query.filter(
            RegistroPonto.colaborador_id == colaborador_id,
            RegistroPonto.data == data
        ).order_by(RegistroPonto.horario.asc()).all()
        
        # Organizar por tipo
        pontos = {}
        for r in registros:
            pontos[r.tipo] = r.horario.strftime('%H:%M:%S')
        
        # Calcular total de horas
        total_horas = RegistroPonto.calcular_horas_trabalhadas(colaborador_id, data)
        
        return {
            'colaborador_id': colaborador_id,
            'data': data.strftime('%Y-%m-%d'),
            'entrada': pontos.get('entrada', '-'),
            'saida_almoco': pontos.get('saida_almoco', '-'),
            'volta_almoco': pontos.get('volta_almoco', '-'),
            'saida': pontos.get('saida', '-'),
            'total_horas': total_horas,
            'registros': [r.to_dict() for r in registros]
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