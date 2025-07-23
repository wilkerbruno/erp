#!/usr/bin/env python3
"""
Script para corrigir problemas nos modelos do banco de dados
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from dotenv import load_dotenv

load_dotenv()

def fix_database_models():
    """Corrige problemas nos modelos do banco"""
    
    environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
    
    print("🔧 CORREÇÃO DOS MODELOS DO BANCO")
    print("="*50)
    print(f"🌍 Ambiente: {environment}")
    
    try:
        app = create_app(environment)
        
        with app.app_context():
            print("🗑️  Removendo tabelas problemáticas...")
            
            # Dropar tabelas específicas que estão causando problema
            try:
                db.session.execute(db.text('DROP TABLE IF EXISTS nao_conformidades'))
                db.session.execute(db.text('DROP TABLE IF EXISTS planos_acao'))
                db.session.execute(db.text('DROP TABLE IF EXISTS auditorias'))
                db.session.execute(db.text('DROP TABLE IF EXISTS itens_auditoria'))
                db.session.commit()
                print("✅ Tabelas problemáticas removidas")
            except Exception as e:
                print(f"⚠️  Aviso ao remover tabelas: {e}")
                db.session.rollback()
            
            print("🔧 Importando modelos corrigidos...")
            
            # Importar modelos para registrá-los
            from app.models import (
                User, Colaborador, NaoConformidade, Auditoria, ItemAuditoria,
                OrdemProducao, Produto, RoteiroProducao, PlanoAcao
            )
            
            print("🛠️  Recriando tabelas...")
            db.create_all()
            
            print("✅ Modelos corrigidos com sucesso!")
            
            # Verificar tabelas criadas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Total de tabelas: {len(tables)}")
            
            # Criar usuário admin
            print("👤 Verificando usuário admin...")
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("🔨 Criando usuário admin...")
                admin = User(
                    username='admin',
                    email='admin@corrigindoarota.com.br',
                    perfil='admin',
                    ativo=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuário admin criado!")
            else:
                print("✅ Usuário admin já existe!")
            
            print("="*50)
            print("🎉 CORREÇÃO CONCLUÍDA!")
            print("📍 Sistema pronto para uso")
            print("🔑 Login: admin / admin123")
            print("="*50)
            
            return True
            
    except Exception as e:
        print(f"❌ Erro durante correção: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_database_models()