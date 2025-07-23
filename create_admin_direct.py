#!/usr/bin/env python3
"""
Script direto para criar admin no Railway
"""

import os
import sys
import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def create_admin_direct():
    """Cria admin diretamente no banco Railway"""
    print("👤 CRIANDO ADMIN DIRETO NO BANCO")
    print("="*40)
    
    # Configurações do Railway
    config = {
        'host': os.environ.get('RAILWAY_DB_HOST'),
        'user': os.environ.get('RAILWAY_DB_USER'),
        'password': os.environ.get('RAILWAY_DB_PASSWORD'),
        'port': int(os.environ.get('RAILWAY_DB_PORT', 3306)),
        'database': os.environ.get('RAILWAY_DB_NAME', 'railway'),
        'charset': 'utf8mb4'
    }
    
    try:
        # Conectar
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Conectado ao Railway")
        
        # Criar tabela users se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                perfil VARCHAR(20) DEFAULT 'user',
                ativo BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        
        # Verificar se admin existe
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_exists = cursor.fetchone()
        
        password_hash = generate_password_hash('admin123')
        
        if admin_exists:
            print("🔄 Admin existe, atualizando...")
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, perfil = 'admin', ativo = 1
                WHERE username = 'admin'
            """, (password_hash,))
        else:
            print("🔨 Criando novo admin...")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, perfil, ativo, created_at)
                VALUES ('admin', 'admin@corrigindoarota.com.br', %s, 'admin', 1, %s)
            """, (password_hash, datetime.utcnow()))
        
        connection.commit()
        
        print("✅ Admin criado/atualizado com sucesso!")
        print("👤 Username: admin")
        print("🔐 Password: admin123")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    create_admin_direct()