import os
import sys

def get_environment():
    """Determina o ambiente baseado nas variáveis disponíveis"""
    
    # Verificar EasyPanel
    if os.getenv('EASYPANEL_PROJECT_ID') or os.getenv('PORT'):
        return 'production'
    
    # Verificar Railway
    if (os.getenv('RAILWAY_DB_HOST') and 
        os.getenv('RAILWAY_DB_PASSWORD')):
        return 'railway'
    
    # Verificar URL do banco
    database_url = os.getenv('DATABASE_URL', '')
    if any(keyword in database_url for keyword in ['railway', 'rlwy.net', 'postgres', 'mysql']):
        return 'production'
    
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
        # Para outros ambientes, assumir que o banco existe
        return True

def fix_import_compatibility():
    """Corrige problemas de compatibilidade de importação"""
    
    try:
        # Tentar importar url_parse da nova localização primeiro
        from urllib.parse import urlparse
        
        # Monkey patch para bibliotecas que ainda usam werkzeug.urls
        import werkzeug.urls
        if not hasattr(werkzeug.urls, 'url_parse'):
            werkzeug.urls.url_parse = urlparse
            print("✅ Compatibilidade werkzeug.urls.url_parse corrigida")
            
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível corrigir compatibilidade: {e}")

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
        return False

def initialize_app():
    """Inicializa a aplicação Flask"""
    
    # Corrigir problemas de compatibilidade primeiro
    fix_import_compatibility()
    
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
        
        # Inicializar Flask-Migrate apenas em desenvolvimento
        if environment == 'development':
            try:
                from flask_migrate import Migrate
                migrate = Migrate(app, db)
                print("✅ Flask-Migrate inicializado!")
            except ImportError:
                print("⚠️  Flask-Migrate não disponível, continuando sem migrations...")
        
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
    """Executa o servidor de produção usando Flask built-in server"""
    
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

# Para compatibilidade com WSGI servers
def create_application():
    """Factory function para WSGI servers como Gunicorn"""
    
    fix_import_compatibility()
    
    try:
        # Importar configuração
        from config import config
        
        environment = get_environment()
        config_class = config.get(environment, config['default'])
        
        print(f"🔧 Usando configuração: {config_class.__name__}")
        
        from app import create_app, db
        
        app = create_app(environment)
        
        # Configurar banco e admin em contexto de aplicação
        with app.app_context():
            try:
                from app.models.user import User
                
                # Criar tabelas se não existirem
                print("🔧 Criando estrutura do banco...")
                db.create_all()
                print("✅ Estrutura criada!")
                
                # Criar admin se não existir
                admin = User.query.filter_by(username='admin').first()
                if not admin:
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
                    print("✅ Admin criado!")
                else:
                    print("✅ Admin já existe!")
                    
            except Exception as e:
                print(f"⚠️  Aviso ao configurar banco: {e}")
                import traceback
                traceback.print_exc()
        
        return app
        
    except Exception as e:
        print(f"❌ Erro ao criar aplicação WSGI: {e}")
        import traceback
        traceback.print_exc()
        raise

# Para Gunicorn e outros WSGI servers
application = create_application()

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