#!/usr/bin/env python3
"""
Script simplificado para criar usuário admin
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_admin():
    """Cria usuário admin de forma simples"""
    
    environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
    
    print("👤 CRIANDO USUÁRIO ADMIN")
    print("="*30)
    
    try:
        app = create_app(environment)
        
        with app.app_context():
            # Usar SQL direto para evitar problemas do modelo
            print("🔍 Verificando se admin existe...")
            
            result = db.session.execute(db.text(
                "SELECT id FROM users WHERE username = 'admin' LIMIT 1"
            )).fetchone()
            
            if result:
                print("⚠️  Usuário admin já existe!")
                
                # Atualizar senha
                print("🔄 Atualizando senha...")
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash('admin123')
                
                db.session.execute(db.text("""
                    UPDATE users 
                    SET password_hash = :password_hash, 
                        perfil = 'admin', 
                        ativo = 1
                    WHERE username = 'admin'
                """), {'password_hash': password_hash})
                
                db.session.commit()
                print("✅ Senha atualizada!")
                
            else:
                print("🔨 Criando novo usuário admin...")
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash('admin123')
                
                db.session.execute(db.text("""
                    INSERT INTO users (username, email, password_hash, perfil, ativo, created_at) 
                    VALUES ('admin', 'admin@corrigindoarota.com.br', :password_hash, 'admin', 1, :created_at)
                """), {
                    'password_hash': password_hash,
                    'created_at': datetime.utcnow()
                })
                
                db.session.commit()
                print("✅ Usuário admin criado!")
            
            # Testar login
            print("🧪 Testando login...")
            from app.models.user import User
            admin = User.query.filter_by(username='admin').first()
            
            if admin and admin.check_password('admin123'):
                print("✅ Teste de login: OK")
                print("\n" + "="*40)
                print("🔑 CREDENCIAIS:")
                print("👤 Username: admin")
                print("🔐 Password: admin123")
                print("="*40)
                return True
            else:
                print("❌ Teste de login: FALHA")
                return False
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_admin()