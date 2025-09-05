#!/usr/bin/env python3
"""
Script para debug do sistema de login
"""
import os
import sys

# Adiciona o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("🔍 TESTANDO CONEXÃO COM BANCO DE DADOS...")
    try:
        import pymysql
        
        connection = pymysql.connect(
            host='easypanel.pontocomdesconto.com.br',
            port=33070,
            user='erp_admin',
            password='8de3405e496812d04fc7',
            database='erp',
            charset='utf8mb4',
            connect_timeout=10
        )
        
        cursor = connection.cursor()
        
        # Verifica se a tabela users existe
        cursor.execute("SHOW TABLES LIKE 'users'")
        result = cursor.fetchone()
        
        if result:
            print("✅ Tabela 'users' encontrada")
            
            # Conta quantos usuários existem
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"👥 Total de usuários: {count}")
            
            if count > 0:
                # Lista os usuários
                cursor.execute("SELECT id, username, email, active FROM users LIMIT 5")
                users = cursor.fetchall()
                print("\n👤 Usuários encontrados:")
                for user in users:
                    print(f"   ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Ativo: {user[3]}")
            else:
                print("⚠️  Nenhum usuário encontrado na tabela")
                
        else:
            print("❌ Tabela 'users' NÃO encontrada")
            
            # Lista todas as tabelas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Tabelas existentes ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_flask_app():
    """Testa aplicação Flask"""
    print("\n🔍 TESTANDO APLICAÇÃO FLASK...")
    
    try:
        # Configura ambiente
        os.environ['FLASK_ENV'] = 'production'  # Para Easy Panel
        
        from config import config
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        app = Flask(__name__)
        app.config.from_object(config['production'])
        
        db = SQLAlchemy(app)
        
        print("✅ Flask app inicializada")
        print(f"🔗 DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Testa se consegue conectar via SQLAlchemy
        with app.app_context():
            try:
                # Tenta executar uma query simples
                result = db.engine.execute("SELECT 1").scalar()
                print(f"✅ SQLAlchemy conectou: resultado = {result}")
                
                # Verifica tabelas via SQLAlchemy
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"📋 Tabelas via SQLAlchemy ({len(tables)}): {tables}")
                
                return True
                
            except Exception as e:
                print(f"❌ Erro SQLAlchemy: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Erro Flask: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_admin_user():
    """Cria usuário admin se não existir"""
    print("\n🔍 VERIFICANDO/CRIANDO USUÁRIO ADMIN...")
    
    try:
        import pymysql
        from werkzeug.security import generate_password_hash
        import hashlib
        
        connection = pymysql.connect(
            host='easypanel.pontocomdesconto.com.br',
            port=33070,
            user='erp_admin',
            password='8de3405e496812d04fc7',
            database='erp',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Verifica se usuário admin existe
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        
        if admin_user:
            print(f"✅ Usuário admin encontrado (ID: {admin_user[0]})")
            
            # Testa hash da senha
            stored_hash = admin_user[2]
            test_password = 'admin123'
            
            from werkzeug.security import check_password_hash
            is_valid = check_password_hash(stored_hash, test_password)
            print(f"🔐 Senha 'admin123' válida: {is_valid}")
            
            if not is_valid:
                print("🔧 Atualizando hash da senha...")
                new_hash = generate_password_hash('admin123')
                cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'admin'", (new_hash,))
                connection.commit()
                print("✅ Senha atualizada!")
        else:
            print("⚠️  Usuário admin não encontrado, criando...")
            
            # Cria usuário admin
            password_hash = generate_password_hash('admin123')
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, active, created_at) 
                VALUES ('admin', 'admin@sistema.com', %s, 1, NOW())
            """, (password_hash,))
            connection.commit()
            print("✅ Usuário admin criado!")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO DO SISTEMA DE LOGIN")
    print("=" * 50)
    
    # Testa conexão
    db_ok = test_database_connection()
    
    if db_ok:
        # Testa Flask
        flask_ok = test_flask_app()
        
        if flask_ok:
            # Cria/verifica admin
            create_admin_user()
    
    print("\n" + "=" * 50)
    print("🏁 DIAGNÓSTICO CONCLUÍDO")