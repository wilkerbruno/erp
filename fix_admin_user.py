#!/usr/bin/env python3
"""
Script para verificar e corrigir o usuário admin
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from dotenv import load_dotenv

load_dotenv()

def fix_admin_user():
    """Corrige o usuário admin"""
    
    # Determinar ambiente
    environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
    
    print("🔧 CORREÇÃO DO USUÁRIO ADMIN")
    print("="*40)
    
    try:
        app = create_app(environment)
        
        with app.app_context():
            # Verificar se o admin existe
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print(f"✅ Admin encontrado: {admin.username}")
                print(f"   - Email: {admin.email}")
                print(f"   - Perfil: {admin.perfil}")
                print(f"   - Ativo: {admin.ativo}")
                print(f"   - Hash existe: {bool(admin.password_hash)}")
                
                # Verificar se a senha funciona
                if admin.check_password('admin123'):
                    print("✅ Senha 'admin123' está correta")
                else:
                    print("❌ Senha 'admin123' NÃO funciona - corrigindo...")
                    admin.set_password('admin123')
                    db.session.commit()
                    print("✅ Senha corrigida!")
                
                # Garantir que está ativo
                if not admin.ativo:
                    print("⚠️  Admin estava inativo - ativando...")
                    admin.ativo = True
                    db.session.commit()
                    print("✅ Admin ativado!")
                
            else:
                print("❌ Admin não encontrado - criando...")
                admin = User(
                    username='admin',
                    email='admin@corrigindoarota.com.br',
                    perfil='admin',
                    ativo=True
                )
                admin.set_password('admin123')
                
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin criado com sucesso!")
            
            # Teste final
            print("\n🧪 TESTE FINAL:")
            final_admin = User.query.filter_by(username='admin').first()
            if final_admin and final_admin.check_password('admin123'):
                print("✅ Login admin/admin123 funcionando!")
                return True
            else:
                print("❌ Ainda há problema com o login!")
                return False
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_admin_user()