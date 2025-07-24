#!/usr/bin/env python3
"""
Script para atualizar configuração com nova conexão Railway
"""

import os
from pathlib import Path

def update_env_file():
    """Atualiza arquivo .env com nova configuração Railway"""
    print("Atualizando arquivo .env...")
    
    env_content = """# Configuracao de Desenvolvimento
FLASK_ENV=railway
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key-mude-em-producao

# Nova configuracao Railway MySQL
RAILWAY_DB_HOST=trolley.proxy.rlwy.net
RAILWAY_DB_USER=root
RAILWAY_DB_PASSWORD=WLarzFFJZhqYAFkIvwcUjBDKoVhaBvJZ
RAILWAY_DB_PORT=19756
RAILWAY_DB_NAME=railway

# URL completa para Railway
DATABASE_URL=mysql+pymysql://root:WLarzFFJZhqYAFkIvwcUjBDKoVhaBvJZ@trolley.proxy.rlwy.net:19756/railway

# Configuracoes da empresa
COMPANY_NAME=Corrigindo à Rota Industria Ltda
COMPANY_EMAIL=contato@corrigindoarota.com.br
"""
    
    with open(".env", 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env atualizado com nova conexão Railway!")

def create_admin_with_new_connection():
    """Cria admin com nova conexão"""
    print("Criando admin com nova conexão...")
    
    admin_script = '''#!/usr/bin/env python3
import os
import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def create_admin():
    """Cria admin na nova conexao Railway"""
    
    config = {
        'host': 'trolley.proxy.rlwy.net',
        'user': 'root',
        'password': 'WLarzFFJZhqYAFkIvwcUjBDKoVhaBvJZ',
        'port': 19756,
        'database': 'railway',
        'charset': 'utf8mb4',
        'connect_timeout': 60,
        'read_timeout': 120,
        'write_timeout': 120,
    }
    
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Conectado ao novo Railway!")
        
        # Criar tabela users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                perfil VARCHAR(20) DEFAULT 'user',
                ativo BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                INDEX idx_username (username),
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # Verificar/criar admin
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_exists = cursor.fetchone()
        
        password_hash = generate_password_hash('admin123')
        
        if admin_exists:
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, perfil = 'admin', ativo = 1
                WHERE username = 'admin'
            """, (password_hash,))
            print("🔄 Admin atualizado!")
        else:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, perfil, ativo, created_at)
                VALUES ('admin', 'admin@corrigindoarota.com.br', %s, 'admin', 1, %s)
            """, (password_hash, datetime.utcnow()))
            print("🔨 Admin criado!")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ Usuário admin configurado!")
        print("👤 Username: admin")
        print("🔐 Password: admin123")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    create_admin()
'''
    
    with open("create_admin_new_railway.py", 'w', encoding='utf-8') as f:
        f.write(admin_script)
    
    print("✅ Script de admin criado!")

def main():
    print("🔄 ATUALIZANDO PARA NOVA CONEXÃO RAILWAY")
    print("="*50)
    
    update_env_file()
    create_admin_with_new_connection()
    
    print("="*50)
    print("✅ ATUALIZAÇÃO CONCLUÍDA!")
    print("Execute:")
    print("1. python create_admin_new_railway.py")
    print("2. python run.py")
    print("="*50)

if __name__ == "__main__":
    main()