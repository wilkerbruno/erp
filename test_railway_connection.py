#!/usr/bin/env python3
"""
Script para testar a conexão com o banco Railway
"""
import os
import pymysql
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_railway_connection():
    """Testa a conexão com o banco Railway"""
    
    # Configurações do Railway
    config = {
        'host': os.environ.get('RAILWAY_DB_HOST'),
        'user': os.environ.get('RAILWAY_DB_USER'),
        'password': os.environ.get('RAILWAY_DB_PASSWORD'),
        'port': int(os.environ.get('RAILWAY_DB_PORT', 3306)),
        'database': os.environ.get('RAILWAY_DB_NAME', 'railway'),
        'charset': 'utf8mb4',
        'connect_timeout': 60,
        'read_timeout': 60,
        'write_timeout': 60,
    }
    
    print("🔗 Testando conexão com Railway MySQL...")
    print(f"📍 Host: {config['host']}")
    print(f"👤 User: {config['user']}")
    print(f"🔌 Port: {config['port']}")
    print(f"🗄️  Database: {config['database']}")
    print("-" * 50)
    
    try:
        # Tentar conectar
        print("⏳ Conectando...")
        connection = pymysql.connect(**config)
        
        print("✅ Conexão estabelecida com sucesso!")
        
        # Testar uma query simples
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION() as version")
            result = cursor.fetchone()
            print(f"📊 Versão do MySQL: {result[0]}")
            
            # Listar databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"🗃️  Databases disponíveis: {[db[0] for db in databases]}")
            
            # Verificar se já existem tabelas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print(f"📋 Tabelas existentes: {[table[0] for table in tables]}")
            else:
                print("📋 Nenhuma tabela encontrada (banco vazio)")
        
        connection.close()
        print("🔐 Conexão fechada.")
        return True
        
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        print("\n🔧 Verifique:")
        print("  - Se as credenciais estão corretas no arquivo .env")
        print("  - Se o serviço Railway está ativo")
        print("  - Se não há firewall bloqueando a porta")
        return False

if __name__ == "__main__":
    test_railway_connection()