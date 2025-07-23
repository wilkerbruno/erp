#!/usr/bin/env python3
"""
Script para verificar o status do banco de dados
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from dotenv import load_dotenv

load_dotenv()

def check_database_status():
    """Verifica o status completo do banco"""
    
    # Determinar ambiente
    env = os.getenv('FLASK_ENV', 'development')
    database_url = os.getenv('DATABASE_URL', '')
    
    if 'railway' in database_url or 'rlwy.net' in database_url:
        environment = 'railway'
    else:
        environment = 'development'
    
    print(f"🔍 VERIFICAÇÃO DO BANCO DE DADOS")
    print("="*50)
    print(f"🌍 Ambiente: {environment}")
    
    try:
        app = create_app(environment)
        print(f"🗄️  URL: {app.config['SQLALCHEMY_DATABASE_URI'][:70]}...")
        
        with app.app_context():
            # Testar conexão
            try:
                db.session.execute(db.text('SELECT 1'))
                print("✅ Conexão: OK")
            except Exception as e:
                print(f"❌ Conexão: FALHA - {e}")
                return False
            
            # Verificar tabelas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tabelas: {len(tables)} encontradas")
            
            if not tables:
                print("⚠️  Nenhuma tabela encontrada! Execute: python init_database.py")
                return False
            
            # Verificar dados
            from app.models import User, CentroCusto, ContaFinanceira, Fornecedor
            
            user_count = User.query.count()
            print(f"👤 Usuários: {user_count}")
            
            if user_count == 0:
                print("⚠️  Nenhum usuário encontrado!")
            else:
                admin = User.query.filter_by(username='admin').first()
                if admin:
                    print(f"✅ Admin: {admin.username} ({admin.email})")
                else:
                    print("⚠️  Usuário admin não encontrado!")
            
            # Outros dados
            print(f"🏢 Centros de Custo: {CentroCusto.query.count()}")
            print(f"💰 Contas Financeiras: {ContaFinanceira.query.count()}")
            print(f"🚛 Fornecedores: {Fornecedor.query.count()}")
            
            print("="*50)
            print("✅ Verificação concluída!")
            return True
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    check_database_status()