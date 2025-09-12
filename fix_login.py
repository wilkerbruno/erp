#!/usr/bin/env python3
"""
Script para corrigir problemas de login no Easy Panel
"""
import os
import sys

def fix_admin_user():
    """Corrige/cria usuário admin"""
    try:
        import pymysql
        from werkzeug.security import generate_password_hash
        
        print("🔧 Conectando ao banco...")
        
        connection = pymysql.connect(
            host='divisions_bhs_erp_bd',
            port=3306,
            user='erp_admin',
            password='8de3405e496812d04fc7',
            database='erp',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Verifica se a tabela users existe
        cursor.execute("SHOW TABLES LIKE 'users'")
        if not cursor.fetchone():
            print("📋 Criando tabela users...")
            cursor.execute("""
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("✅ Tabela users criada!")
        
        # Remove usuário admin existente
        cursor.execute("DELETE FROM users WHERE username = 'admin'")
        
        # Cria novo usuário admin
        password_hash = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, active, created_at)
            VALUES ('admin', 'admin@sistema.com', %s, 1, NOW())
        """, (password_hash,))
        
        connection.commit()
        print("✅ Usuário admin criado/atualizado!")
        print("👤 Username: admin")
        print("🔐 Password: admin123")
        
        # Verifica criação
        cursor.execute("SELECT id, username, email, active FROM users WHERE username = 'admin'")
        user = cursor.fetchone()
        if user:
            print(f"✅ Verificação OK: ID={user[0]}, Username={user[1]}, Email={user[2]}, Ativo={user[3]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def create_env_file():
    """Cria arquivo .env para Easy Panel"""
    env_content = """# Easy Panel Configuration
FLASK_ENV=production
FLASK_DEBUG=false
DATABASE_URL=mysql+pymysql://erp_admin:8de3405e496812d04fc7@divisions_bhs_erp_bd:3306/erp
SECRET_KEY=easypanel-secret-key-2024
MYSQL_HOST=divisions_bhs_erp_bd
MYSQL_PORT=3306
MYSQL_USER=erp_admin
MYSQL_PASSWORD=8de3405e496812d04fc7
MYSQL_DATABASE=erp
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def test_login_manually():
    """Testa login manualmente"""
    try:
        from werkzeug.security import check_password_hash
        import pymysql
        
        connection = pymysql.connect(
            host='divisions_bhs_erp_bd',
            port=3306,
            user='erp_admin',
            password='8de3405e496812d04fc7',
            database='erp',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT username, password_hash, active FROM users WHERE username = 'admin'")
        user = cursor.fetchone()
        
        if user:
            username, password_hash, active = user
            print(f"👤 Usuário: {username}")
            print(f"🔓 Ativo: {active}")
            
            # Testa senha
            is_valid = check_password_hash(password_hash, 'admin123')
            print(f"🔐 Senha 'admin123' válida: {is_valid}")
            
            if is_valid and active:
                print("✅ Login deve funcionar!")
                return True
            else:
                print("❌ Problema no login detectado")
                return False
        else:
            print("❌ Usuário admin não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CORRIGINDO PROBLEMAS DE LOGIN")
    print("=" * 50)
    
    # Corrige usuário admin
    if fix_admin_user():
        print("\n" + "-" * 30)
        
        # Cria .env
        create_env_file()
        
        print("\n" + "-" * 30)
        
        # Testa login
        test_login_manually()
    
    print("\n" + "=" * 50)
    print("🏁 CORREÇÃO CONCLUÍDA")
    print("\nAgora tente fazer login com:")
    print("👤 Usuário: admin")
    print("🔐 Senha: admin123")