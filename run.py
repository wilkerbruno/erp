#!/usr/bin/env python3
"""
Script principal corrigido para iniciar a aplicação Flask
"""
import os
import sys
from flask_migrate import Migrate

def get_environment():
    """Determina o ambiente baseado nas variáveis disponíveis"""
    
    # Verificar se é Railway
    if (os.getenv('RAILWAY_DB_HOST') and 
        os.getenv('RAILWAY_DB_PASSWORD')):
        return 'railway'
    
    # Verificar URL do banco
    database_url = os.getenv('DATABASE_URL', '')
    if 'railway' in database_url or 'rlwy.net' in database_url:
        return 'railway'
    
    # Verificar se tem arquivo de configuração específico
    if os.path.exists('config.py'):
        return 'development'
    
    # Default
    return 'development'

def ensure_database_exists():
    """Garante que o banco de dados existe e tem a estrutura necessária"""
    
    environment = get_environment()
    
    if environment == 'development':
        # Para SQLite, garantir que o diretório instance existe
        os.makedirs('instance', exist_ok=True)
        
        db_file = 'instance/app.db'
        if not os.path.exists(db_file):
            print(f"🔧 Banco {db_file} não existe, será criado automaticamente")
            
        return True
    else:
        # Para outros ambientes (Railway), assumir que o banco existe
        return True

def create_admin_safely(app):
    """Cria usuário admin de forma segura"""
    
    try:
        with app.app_context():
            from app import db
            from app.models.user import User
            
            # Verificar se as tabelas existem
            try:
                # Tentar uma query simples para verificar se a tabela existe
                User.query.first()
                print("✅ Tabela 'users' encontrada")
                
            except Exception as table_error:
                print(f"🔧 Tabela 'users' não encontrada, criando estrutura...")
                
                try:
                    # Criar todas as tabelas
                    db.create_all()
                    print("✅ Estrutura do banco criada!")
                    
                except Exception as create_error:
                    print(f"❌ Erro ao criar estrutura: {create_error}")
                    return False
            
            # Verificar/criar admin
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print("✅ Usuário admin já existe!")
                
                # Verificar se a senha está funcionando
                if not admin.password_hash:
                    print("🔧 Admin sem senha, corrigindo...")
                    admin.set_password('admin123')
                    admin.perfil = 'admin'
                    admin.ativo = True
                    db.session.commit()
                    print("✅ Senha do admin corrigida!")
                    
            else:
                print("🔧 Criando usuário admin...")
                
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
            
            return True
            
    except Exception as e:
        print(f"❌ Erro geral ao criar admin: {e}")
        
        # Fallback: tentar criar via SQL direto (só para SQLite)
        try:
            environment = get_environment()
            if environment == 'development':
                print("🔧 Tentando fallback com SQLite...")
                return create_admin_sqlite_fallback()
            else:
                return False
                
        except Exception as fallback_error:
            print(f"❌ Fallback também falhou: {fallback_error}")
            return False

def create_admin_sqlite_fallback():
    """Fallback para criar admin diretamente no SQLite"""
    
    try:
        import sqlite3
        from werkzeug.security import generate_password_hash
        
        db_file = 'instance/app.db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Criar tabela se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                perfil VARCHAR(20) DEFAULT 'user',
                ativo BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        
        # Verificar se admin existe
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            password_hash = generate_password_hash('admin123')
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, perfil, ativo)
                VALUES ('admin', 'admin@corrigindoarota.com.br', ?, 'admin', 1)
            """, (password_hash,))
            print("✅ Admin criado via SQLite!")
        else:
            print("✅ Admin já existe no SQLite!")
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Falha no fallback SQLite: {e}")
        return False

def initialize_app():
    """Inicializa a aplicação Flask"""
    
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente detectado: {environment}")
    
    # Garantir que o banco existe
    if not ensure_database_exists():
        print("❌ Falha ao configurar banco de dados!")
        return None
    
    # Importar e criar app
    try:
        from app import create_app, db
        
        app = create_app(environment)
        
        # Inicializar Flask-Migrate
        migrate = Migrate(app, db)
        
        print("✅ Aplicação Flask criada com sucesso!")
        
        # Mostrar blueprints registrados
        blueprints = list(app.blueprints.keys())
        print(f"📋 Blueprints registrados ({len(blueprints)}): {', '.join(blueprints)}")
        
        return app
        
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_development_server(app):
    """Executa o servidor de desenvolvimento"""
    
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("="*60)
    print("🚀 INICIANDO SERVIDOR DE DESENVOLVIMENTO")
    print("="*60)
    print(f"🌍 Ambiente: {get_environment()}")
    print(f"🔗 URL: http://localhost:{port}")
    print(f"👤 Login: admin")
    print(f"🔐 Senha: admin123")
    print("="*60)
    print("💡 Pressione Ctrl+C para parar o servidor")
    print("="*60)
    
    try:
        app.run(
            host=host,
            port=port,
            debug=True,
            use_reloader=False,  # Evitar recarregamento duplo
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no servidor: {e}")

def run_production_server(app):
    """Executa o servidor de produção"""
    
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("="*60)
    print("🚀 INICIANDO SERVIDOR DE PRODUÇÃO")
    print("="*60)
    print(f"🔗 Host: {host}:{port}")
    print("="*60)
    
    try:
        app.run(
            host=host,
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")

def main():
    """Função principal"""
    
    print("🔧 SISTEMA ERP - CORRIGINDO À ROTA")
    print("="*50)
    
    # Inicializar aplicação
    app = initialize_app()
    if not app:
        print("❌ Falha crítica na inicialização!")
        return False
    
    # Configurar banco e admin
    admin_created = create_admin_safely(app)
    if not admin_created:
        print("⚠️  Aviso: Problemas na criação do admin, mas continuando...")
    
    # Determinar tipo de servidor
    environment = get_environment()
    
    if environment == 'development':
        run_development_server(app)
    else:
        run_production_server(app)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            print("\n❌ Sistema encerrado com erros!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)