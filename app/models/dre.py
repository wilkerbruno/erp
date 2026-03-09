from app import db
from datetime import datetime

class DREGerencial(db.Model):
    """Modelo de DRE Gerencial"""
    __tablename__ = 'dre_gerencial'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Competência
    mes = db.Column(db.Integer, nullable=False)  # 1-12
    ano = db.Column(db.Integer, nullable=False)
    
    # RECEITAS
    receita_bruta = db.Column(db.Numeric(15, 2), default=0)
    deducoes = db.Column(db.Numeric(15, 2), default=0)
    receita_liquida = db.Column(db.Numeric(15, 2), default=0)
    
    # CUSTOS
    custo_mercadorias = db.Column(db.Numeric(15, 2), default=0)
    custo_servicos = db.Column(db.Numeric(15, 2), default=0)
    lucro_bruto = db.Column(db.Numeric(15, 2), default=0)
    
    # DESPESAS OPERACIONAIS
    # Vendas
    despesas_vendas = db.Column(db.Numeric(15, 2), default=0)
    comissoes_vendas = db.Column(db.Numeric(15, 2), default=0)
    
    # Administrativas
    despesas_administrativas = db.Column(db.Numeric(15, 2), default=0)
    salarios_encargos = db.Column(db.Numeric(15, 2), default=0)
    aluguel = db.Column(db.Numeric(15, 2), default=0)
    
    # Financeiras
    despesas_financeiras = db.Column(db.Numeric(15, 2), default=0)
    receitas_financeiras = db.Column(db.Numeric(15, 2), default=0)
    
    # RESULTADO
    resultado_operacional = db.Column(db.Numeric(15, 2), default=0)
    impostos_contribuicoes = db.Column(db.Numeric(15, 2), default=0)
    resultado_liquido = db.Column(db.Numeric(15, 2), default=0)
    
    # INDICADORES
    margem_bruta = db.Column(db.Numeric(5, 2))  # %
    margem_operacional = db.Column(db.Numeric(5, 2))  # %
    margem_liquida = db.Column(db.Numeric(5, 2))  # %
    
    # Metadados
    observacoes = db.Column(db.Text)
    importado_de = db.Column(db.String(100))  # 'contador', 'sistema', 'manual'
    arquivo_origem = db.Column(db.String(500))
    
    # Auditoria
    criado_por = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    criador = db.relationship('User', foreign_keys=[criado_por])
    
    def __repr__(self):
        return f'<DREGerencial {self.mes}/{self.ano}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'mes': self.mes,
            'ano': self.ano,
            'receita_bruta': float(self.receita_bruta),
            'receita_liquida': float(self.receita_liquida),
            'lucro_bruto': float(self.lucro_bruto),
            'resultado_liquido': float(self.resultado_liquido),
            'margem_bruta': float(self.margem_bruta) if self.margem_bruta else None,
            'margem_liquida': float(self.margem_liquida) if self.margem_liquida else None
        }
