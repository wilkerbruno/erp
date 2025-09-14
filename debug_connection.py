#!/usr/bin/env python3
"""
Script para testar conexão com banco EasyPanel
Execute este script para verificar se a conexão está funcionando
"""

import os
import sys
from sqlalchemy import create_engine, text
import traceback

def test_easypanel_connection():
    """Testa a conexão com o banco EasyPanel"""
    
    # Dados de conexão EasyPanel
    config = {
        'host': 'easypanel.pontocomdesconto.com.br',
        'port': 33070,
        'user': 'erp_admin',
        'password': '8de3405e496812d04fc7',
        'database': 'erp'
    }
    
    print("🔧 TESTE DE CONEXÃO - EASYPANEL MYSQL")
    print("="*50)
    print(f"Host: {config['host']}")
    print(f"Porta: {config['port']}")
    print(f"Usuário: {config['user']}")
    print(f"Banco: {config['database']}")
    print("="*50)
    
    # Montar URL de conexão
    db_url = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    
    try:
        print("🔌 Tentando conectar...")
        
        # Criar engine
        engine = create_engine(
            db_url,
            pool_timeout=30,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=True,  # Mostrar queries SQL
            connect_args={
                'charset': 'utf8mb4',
                'connect_timeout': 60,
                'read_timeout': 30,
                'write_timeout': 30
            }
        )
        
        # Testar conexão
        with engine.connect() as connection:
            print("✅ Conexão estabelecida!")
            
            # Teste básico
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            print(f"✅ Teste básico: {test_value}")
            
            # Verificar versão MySQL
            result = connection.execute(text("SELECT VERSION() as version"))
            version = result.fetchone()[0]
            print(f"✅ Versão MySQL: {version}")
            
            # Listar tabelas
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Tabelas encontradas ({len(tables)}): {', '.join(tables) if tables else 'Nenhuma'}")
            
            # Verificar charset
            result = connection.execute(text("SELECT @@character_set_database as charset"))
            charset = result.fetchone()[0]
            print(f"✅ Charset: {charset}")
            
            print("\n🎉 CONEXÃO COM EASYPANEL OK!")
            return True
            
    except Exception as e:
        print(f"\n❌ ERRO NA CONEXÃO: {e}")
        print("\n🔍 Detalhes do erro:")
        traceback.print_exc()
        
        print("\n💡 Possíveis soluções:")
        print("1. Verificar se o banco está online no EasyPanel")
        print("2. Verificar credenciais (usuário/senha)")
        print("3. Verificar se a porta 33070 está acessível")
        print("4. Verificar configuração de firewall")
        
        return False

def test_with_flask_config():
    """Testa usando a configuração do Flask"""
    
    print("\n" + "="*50)
    print("🔧 TESTE COM CONFIGURAÇÃO DO FLASK")
    print("="*50)
    
    try:
        # Definir variáveis de ambiente
        os.environ['DB_HOST'] = 'easypanel.pontocomdesconto.com.br'
        os.environ['DB_PORT'] = '33070'
        os.environ['DB_USER'] = 'erp_admin'
        os.environ['DB_PASSWORD'] = '8de3405e496812d04fc7'
        os.environ['DB_NAME'] = 'erp'
        
        # Importar config
        from config import config
        
        # Usar configuração externa
        config_class = config['external']
        
        # Criar instância de configuração
        app_config = config_class()
        
        db_uri = app_config.SQLALCHEMY_DATABASE_URI
        print(f"📊 Database URI: {db_uri}")
        
        # Testar com a configuração
        engine = create_engine(
            db_uri,
            **app_config.SQLALCHEMY_ENGINE_OPTIONS
        )
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 'Flask Config OK' as test"))
            message = result.fetchone()[0]
            print(f"✅ {message}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro com config Flask: {e}")
        traceback.print_exc()
        return False

def main():
    """Função principal de teste"""
    
    print("🏢 ERP CORRIGINDO À ROTA - TESTE DE CONEXÃO")
    print("="*60)
    
    # Teste direto
    direct_ok = test_easypanel_connection()
    
    # Teste com Flask config
    flask_ok = test_with_flask_config()
    
    print("\n" + "="*60)
    print("📋 RESULTADO DOS TESTES")
    print("="*60)
    print(f"Conexão direta: {'✅ OK' if direct_ok else '❌ FALHOU'}")
    print(f"Config Flask: {'✅ OK' if flask_ok else '❌ FALHOU'}")
    
    if direct_ok and flask_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("💡 Sua aplicação deve funcionar no EasyPanel")
        return True
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("💡 Verifique a configuração antes de fazer deploy")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro crítico: {e}")
        traceback.print_exc()
        sys.exit(1)