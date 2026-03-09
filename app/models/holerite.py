from app import db
from datetime import datetime

class Holerite(db.Model):
    """Modelo de Holerite"""
    __tablename__ = 'holerite'
    
    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    
    # Competência
    mes = db.Column(db.Integer, nullable=False)  # 1-12
    ano = db.Column(db.Integer, nullable=False)
    
    # Vencimentos
    salario_base = db.Column(db.Numeric(10, 2), default=0)
    horas_extras = db.Column(db.Numeric(10, 2), default=0)
    adicional_noturno = db.Column(db.Numeric(10, 2), default=0)
    comissoes = db.Column(db.Numeric(10, 2), default=0)
    bonus = db.Column(db.Numeric(10, 2), default=0)
    
    # Benefícios
    vale_alimentacao = db.Column(db.Numeric(10, 2), default=0)
    vale_transporte = db.Column(db.Numeric(10, 2), default=0)
    auxilio_celular = db.Column(db.Numeric(10, 2), default=0)
    plano_saude = db.Column(db.Numeric(10, 2), default=0)
    outros_beneficios = db.Column(db.Numeric(10, 2), default=0)
    
    total_vencimentos = db.Column(db.Numeric(10, 2), default=0)
    
    # Descontos
    inss = db.Column(db.Numeric(10, 2), default=0)
    irrf = db.Column(db.Numeric(10, 2), default=0)
    vale_transporte_desconto = db.Column(db.Numeric(10, 2), default=0)
    plano_saude_desconto = db.Column(db.Numeric(10, 2), default=0)
    faltas = db.Column(db.Numeric(10, 2), default=0)
    atrasos = db.Column(db.Numeric(10, 2), default=0)
    adiantamento = db.Column(db.Numeric(10, 2), default=0)
    emprestimos = db.Column(db.Numeric(10, 2), default=0)
    outros_descontos = db.Column(db.Numeric(10, 2), default=0)
    
    total_descontos = db.Column(db.Numeric(10, 2), default=0)
    
    # Líquido
    liquido = db.Column(db.Numeric(10, 2), default=0)
    
    # Base de cálculo
    base_inss = db.Column(db.Numeric(10, 2), default=0)
    base_irrf = db.Column(db.Numeric(10, 2), default=0)
    base_fgts = db.Column(db.Numeric(10, 2), default=0)
    
    # FGTS
    fgts = db.Column(db.Numeric(10, 2), default=0)
    
    # Observações
    observacoes = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(20), default='gerado')  # 'gerado', 'enviado', 'pago'
    data_pagamento = db.Column(db.Date)
    
    # Auditoria
    gerado_por = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    colaborador = db.relationship('Colaborador', backref='holerites')
    gerador = db.relationship('User', foreign_keys=[gerado_por])
    
    def __repr__(self):
        return f'<Holerite {self.colaborador_id} - {self.mes}/{self.ano}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'colaborador_id': self.colaborador_id,
            'mes': self.mes,
            'ano': self.ano,
            'salario_base': float(self.salario_base),
            'total_vencimentos': float(self.total_vencimentos),
            'total_descontos': float(self.total_descontos),
            'liquido': float(self.liquido),
            'status': self.status
        }
