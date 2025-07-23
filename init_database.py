#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do ERP Corrigindo à Rota
- Cria todas as tabelas
- Insere usuário administrador
- Insere dados básicos do sistema
"""

import os
import sys
from datetime import datetime, date
from decimal import Decimal

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def get_environment():
    """Determina o ambiente de execução"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    database_url = os.getenv('DATABASE_URL', '')
    
    if 'railway' in database_url or 'rlwy.net' in database_url:
        return 'railway'
    elif env in ['production', 'prod']:
        return 'production'
    elif env in ['testing', 'test']:
        return 'testing'
    else:
        return 'development'

def test_connection(app):
    """Testa a conexão com o banco de dados"""
    try:
        with app.app_context():
            result = db.session.execute(db.text('SELECT 1')).scalar()
            if result == 1:
                return True
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def drop_all_tables(app):
    """Remove todas as tabelas (use com cuidado!)"""
    try:
        with app.app_context():
            print("🗑️  Removendo todas as tabelas...")
            db.drop_all()
            print("✅ Tabelas removidas com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao remover tabelas: {e}")
        return False

def create_all_tables(app):
    """Cria todas as tabelas do banco"""
    try:
        with app.app_context():
            print("🔧 Criando tabelas do banco de dados...")
            
            # Importar todos os modelos para garantir que sejam registrados
            from app.models import (
                User, Colaborador, NaoConformidade, Auditoria, ItemAuditoria,
                OrdemProducao, Produto, RoteiroProducao, PlanoAcao,
                ProjetoConsultoria, ProdutoConsultoria, OrdemCompra, 
                ItemOrdemCompra, Fornecedor, NotaFiscal, ContaFinanceira, 
                LancamentoFinanceiro, CentroCusto, Equipamento, OrdemServico, 
                PlanoManutencao, Projeto, TarefaProjeto, Reuniao, PICS
            )
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Listar tabelas criadas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tabelas criadas: {len(tables)}")
            for table in sorted(tables):
                print(f"   - {table}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_admin_user(app):
    """Cria usuário administrador"""
    try:
        with app.app_context():
            from app.models.user import User
            
            print("👤 Verificando usuário administrador...")
            
            # Verificar se já existe
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("ℹ️  Usuário admin já existe!")
                print(f"   - ID: {admin.id}")
                print(f"   - Email: {admin.email}")
                print(f"   - Perfil: {admin.perfil}")
                print(f"   - Ativo: {admin.ativo}")
                return True
            
            # Criar novo usuário admin
            print("🔨 Criando usuário administrador...")
            admin = User(
                username='admin',
                email='admin@corrigindoarota.com.br',
                perfil='admin',
                ativo=True
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuário administrador criado com sucesso!")
            print("📧 Email: admin@corrigindoarota.com.br")
            print("🔑 Username: admin")
            print("🔐 Password: admin123")
            print("👑 Perfil: admin")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass
        return False

def create_basic_data(app):
    """Cria dados básicos do sistema"""
    try:
        with app.app_context():
            print("📊 Criando dados básicos do sistema...")
            
            # Importar modelos necessários
            from app.models.financeiro import CentroCusto, ContaFinanceira
            from app.models.compras import Fornecedor
            from app.models.producao import Produto
            from app.models.consultoria import ProdutoConsultoria
            
            # Centros de Custo
            centros_custo = [
                {'codigo': 'ADM', 'nome': 'Administrativo', 'descricao': 'Despesas administrativas'},
                {'codigo': 'PROD', 'nome': 'Produção', 'descricao': 'Custos de produção'},
                {'codigo': 'VEN', 'nome': 'Vendas', 'descricao': 'Custos de vendas'},
                {'codigo': 'MKT', 'nome': 'Marketing', 'descricao': 'Despesas de marketing'},
            ]
            
            for cc_data in centros_custo:
                if not CentroCusto.query.filter_by(codigo=cc_data['codigo']).first():
                    cc = CentroCusto(**cc_data)
                    db.session.add(cc)
            
            # Contas Financeiras (Plano de Contas Básico)
            contas = [
                # RECEITAS
                {'codigo': '3.1.01', 'nome': 'Vendas de Produtos', 'tipo': 'receita', 'natureza': 'credito'},
                {'codigo': '3.1.02', 'nome': 'Prestação de Serviços', 'tipo': 'receita', 'natureza': 'credito'},
                {'codigo': '3.2.01', 'nome': 'Receitas Financeiras', 'tipo': 'receita', 'natureza': 'credito'},
                
                # DESPESAS
                {'codigo': '4.1.01', 'nome': 'Custo dos Produtos Vendidos', 'tipo': 'despesa', 'natureza': 'debito'},
                {'codigo': '4.2.01', 'nome': 'Salários e Encargos', 'tipo': 'despesa', 'natureza': 'debito'},
                {'codigo': '4.2.02', 'nome': 'Aluguel', 'tipo': 'despesa', 'natureza': 'debito'},
                {'codigo': '4.2.03', 'nome': 'Energia Elétrica', 'tipo': 'despesa', 'natureza': 'debito'},
                {'codigo': '4.2.04', 'nome': 'Telefone/Internet', 'tipo': 'despesa', 'natureza': 'debito'},
                {'codigo': '4.2.05', 'nome': 'Material de Escritório', 'tipo': 'despesa', 'natureza': 'debito'},
                {'codigo': '4.3.01', 'nome': 'Despesas Financeiras', 'tipo': 'despesa', 'natureza': 'debito'},
                
                # ATIVOS
                {'codigo': '1.1.01', 'nome': 'Caixa', 'tipo': 'ativo', 'natureza': 'debito'},
                {'codigo': '1.1.02', 'nome': 'Banco Conta Corrente', 'tipo': 'ativo', 'natureza': 'debito'},
                {'codigo': '1.2.01', 'nome': 'Estoque de Produtos', 'tipo': 'ativo', 'natureza': 'debito'},
                {'codigo': '1.3.01', 'nome': 'Máquinas e Equipamentos', 'tipo': 'ativo', 'natureza': 'debito'},
                
                # PASSIVOS
                {'codigo': '2.1.01', 'nome': 'Fornecedores', 'tipo': 'passivo', 'natureza': 'credito'},
                {'codigo': '2.1.02', 'nome': 'Salários a Pagar', 'tipo': 'passivo', 'natureza': 'credito'},
                {'codigo': '2.2.01', 'nome': 'Financiamentos', 'tipo': 'passivo', 'natureza': 'credito'},
            ]
            
            for conta_data in contas:
                if not ContaFinanceira.query.filter_by(codigo=conta_data['codigo']).first():
                    conta = ContaFinanceira(**conta_data)
                    db.session.add(conta)
            
            # Fornecedores Exemplo
            fornecedores = [
                {
                    'nome': 'Fornecedor ABC Ltda',
                    'cnpj': '12.345.678/0001-90',
                    'email': 'contato@fornecedorabc.com.br',
                    'telefone': '(11) 3000-0000',
                    'cidade': 'São Paulo',
                    'estado': 'SP'
                },
                {
                    'nome': 'Eletrônicos DEF S.A.',
                    'cnpj': '98.765.432/0001-10',
                    'email': 'vendas@eletronicosdef.com.br',
                    'telefone': '(11) 4000-0000',
                    'cidade': 'Guarulhos',
                    'estado': 'SP'
                }
            ]
            
            for forn_data in fornecedores:
                if not Fornecedor.query.filter_by(cnpj=forn_data['cnpj']).first():
                    fornecedor = Fornecedor(**forn_data)
                    db.session.add(fornecedor)
            
            # Produtos Exemplo
            produtos = [
                {
                    'codigo': 'PROD001',
                    'nome': 'Produto A',
                    'descricao': 'Produto exemplo A',
                    'unidade_medida': 'UN',
                    'preco_custo': Decimal('50.00'),
                    'preco_venda': Decimal('75.00')
                },
                {
                    'codigo': 'PROD002',
                    'nome': 'Produto B',
                    'descricao': 'Produto exemplo B',
                    'unidade_medida': 'KG',
                    'preco_custo': Decimal('25.00'),
                    'preco_venda': Decimal('40.00')
                }
            ]
            
            for prod_data in produtos:
                if not Produto.query.filter_by(codigo=prod_data['codigo']).first():
                    produto = Produto(**prod_data)
                    db.session.add(produto)
            
            # Produtos de Consultoria
            produtos_consultoria = [
                {
                    'nome': 'GRD - Shop Floor Management',
                    'descricao': 'Implementação de Gestão de Rotina no chão de fábrica',
                    'duracao_estimada': 90,
                    'valor_base': Decimal('50000.00')
                },
                {
                    'nome': 'DRE Gerencial',
                    'descricao': 'Implementação de DRE Gerencial com indicadores',
                    'duracao_estimada': 60,
                    'valor_base': Decimal('35000.00')
                },
                {
                    'nome': 'Programa Excelência Integrada',
                    'descricao': 'Programa completo de excelência operacional',
                    'duracao_estimada': 180,
                    'valor_base': Decimal('120000.00')
                }
            ]
            
            for prod_cons_data in produtos_consultoria:
                if not ProdutoConsultoria.query.filter_by(nome=prod_cons_data['nome']).first():
                    produto_cons = ProdutoConsultoria(**prod_cons_data)
                    db.session.add(produto_cons)
            
            # Salvar todas as alterações
            db.session.commit()
            print("✅ Dados básicos criados com sucesso!")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar dados básicos: {e}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass
        return False

def show_summary(app):
    """Mostra resumo do banco de dados"""
    try:
        with app.app_context():
            print("\n" + "="*60)
            print("📊 RESUMO DO BANCO DE DADOS")
            print("="*60)
            
            # Contar registros em cada tabela
            from app.models import User, Colaborador, CentroCusto, ContaFinanceira, Fornecedor, Produto, ProdutoConsultoria
            
            counts = {
                'Usuários': User.query.count(),
                'Colaboradores': Colaborador.query.count(),
                'Centros de Custo': CentroCusto.query.count(),
                'Contas Financeiras': ContaFinanceira.query.count(),
                'Fornecedores': Fornecedor.query.count(),
                'Produtos': Produto.query.count(),
                'Produtos de Consultoria': ProdutoConsultoria.query.count(),
            }
            
            for table, count in counts.items():
                print(f"📋 {table}: {count} registros")
            
            print("="*60)
            print("🎉 SISTEMA PRONTO PARA USO!")
            print("📍 Acesse: http://localhost:5000")
            print("🔑 Login: admin / admin123")
            print("="*60)
            
    except Exception as e:
        print(f"❌ Erro ao gerar resumo: {e}")

def main():
    """Função principal"""
    print("🚀 INICIALIZADOR DO BANCO ERP CORRIGINDO À ROTA")
    print("="*60)
    
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente: {environment}")
    
    # Criar aplicação
    try:
        app = create_app(environment)
        print(f"✅ Aplicação criada")
        print(f"🗄️  Banco: {app.config['SQLALCHEMY_DATABASE_URI'][:80]}...")
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        return False
    
    # Testar conexão
    print("\n🔗 Testando conexão com banco...")
    if not test_connection(app):
        print("❌ Falha na conexão com banco de dados!")
        return False
    print("✅ Conexão OK!")
    
    # Perguntar se quer resetar (apenas se já existem tabelas)
    try:
        with app.app_context():
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if existing_tables:
                print(f"\n⚠️  ATENÇÃO: Encontradas {len(existing_tables)} tabelas existentes:")
                for table in existing_tables[:5]:  # Mostrar apenas as primeiras 5
                    print(f"   - {table}")
                if len(existing_tables) > 5:
                    print(f"   ... e mais {len(existing_tables) - 5} tabelas")
                
                response = input("\n🤔 Deseja RESETAR o banco (apagar tudo)? [s/N]: ").lower()
                if response in ['s', 'sim', 'y', 'yes']:
                    if not drop_all_tables(app):
                        return False
    except Exception as e:
        print(f"⚠️  Aviso: Erro ao verificar tabelas existentes: {e}")
    
    # Criar tabelas
    print("\n🔧 Criando estrutura do banco...")
    if not create_all_tables(app):
        return False
    
    # Criar usuário admin
    print("\n👤 Configurando usuário administrador...")
    if not create_admin_user(app):
        return False
    
    # Criar dados básicos
    print("\n📊 Inserindo dados básicos...")
    if not create_basic_data(app):
        print("⚠️  Aviso: Falha ao criar alguns dados básicos (não crítico)")
    
    # Mostrar resumo
    show_summary(app)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Inicialização concluída com sucesso!")
            print("💡 Para iniciar o sistema: python run.py")
        else:
            print("\n❌ Falha na inicialização!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⛔ Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)