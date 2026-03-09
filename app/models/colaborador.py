from app import db
from datetime import datetime

class Colaborador(db.Model):
    """Modelo de Colaborador"""
    __tablename__ = 'colaborador'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Dados pessoais
    nome_completo = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False, index=True)
    rg = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    sexo = db.Column(db.String(1))  # M, F
    estado_civil = db.Column(db.String(20))
    
    # Contato
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    
    # Endereço
    endereco = db.Column(db.String(200))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(10))
    
    # Dados profissionais
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'))
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'))
    matricula = db.Column(db.String(20), unique=True)
    data_admissao = db.Column(db.Date, nullable=False)
    data_demissao = db.Column(db.Date)
    tipo_contrato = db.Column(db.String(20))  # CLT, PJ, Estagiário
    jornada_trabalho = db.Column(db.String(50))  # 44h semanais, etc
    
    # Salário e benefícios
    salario_base = db.Column(db.Numeric(10, 2))
    
    # Banco
    banco = db.Column(db.String(100))
    agencia = db.Column(db.String(20))
    conta = db.Column(db.String(20))
    tipo_conta = db.Column(db.String(20))  # Corrente, Poupança
    pix = db.Column(db.String(100))
    
    # Horário de trabalho
    horario_entrada = db.Column(db.Time)
    horario_saida = db.Column(db.Time)
    horario_almoco_inicio = db.Column(db.Time)
    horario_almoco_fim = db.Column(db.Time)
    
    # Dados de acesso ao sistema
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cargo = db.relationship('Cargo', backref='colaboradores')
    departamento = db.relationship('Departamento', backref='colaboradores')
    usuario = db.relationship('User', foreign_keys=[usuario_id], backref='colaborador_vinculado')
    
    def __repr__(self):
        return f'<Colaborador {self.nome_completo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'cargo': self.cargo.nome if self.cargo else None,
            'cargo_id': self.cargo_id,
            'departamento': self.departamento.nome if self.departamento else None,
            'departamento_id': self.departamento_id,
            'matricula': self.matricula,
            'data_admissao': self.data_admissao.isoformat() if self.data_admissao else None,
            'salario_base': float(self.salario_base) if self.salario_base else None,
            'ativo': self.ativo
        }
