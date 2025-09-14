import os
import sys
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

def get_environment():
    """Determina o ambiente baseado nas variáveis disponíveis"""
    
    # FORÇAR CONFIGURAÇÃO EXTERNA para EasyPanel
    # Se estamos rodando em produção ou temos PORT definida (EasyPanel)
    if os.getenv('PORT') or os.getenv('EASYPANEL_PROJECT_ID'):
        print("🔧 Detectado ambiente EasyPanel - usando configuração externa")
        return 'external'  # Forçar uso da configuração externa
    
    # Verificar outras plataformas
    if os.getenv('RAILWAY_DB_HOST'):
        return 'railway'
    
    # Verificar URL do banco
    database_url = os.getenv('DATABASE_URL', '')
    if any(keyword in database_url for keyword in ['railway', 'rlwy.net', 'postgres', 'mysql']):
        return 'external'  # Forçar externo para qualquer serviço cloud
    
    # Para desenvolvimento local
    return 'development'

def test_database_connection():
    """Testa a conexão com o banco antes de inicializar"""
    
    try:
        from sqlalchemy import create_engine
        
        # Dados do EasyPanel
        db_url = "mysql+pymysql://erp_admin:8de3405e496812d04fc7@easypanel.pontocomdesconto.com.br:33070/erp"
        
        print("🔧 Testando conexão com banco EasyPanel...")
        print(f"   Host: easypanel.pontocomdesconto.com.br:33070")
        print(f"   Database: erp")
        
        engine = create_engine(
            db_url,
            pool_timeout=30,
            pool_recycle=3600,
            pool_pre_ping=True,
            connect_args={
                'charset': 'utf8mb4',
                'connect_timeout': 60,
                'read_timeout': 30,
                'write_timeout': 30
            }
        )
        
        connection = engine.connect()
        result = connection.execute("SELECT 1 as test")
        test_value = result.fetchone()[0]
        connection.close()
        
        if test_value == 1:
            print("✅ Conexão com banco EasyPanel OK!")
            return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        print("🔧 Verifique se:")
        print("   - O banco está online no EasyPanel")
        print("   - As credenciais estão corretas")
        print("   - A porta 33070 está acessível")
        return False

def ensure_database_exists():
    """Garante que o banco de dados existe e tem a estrutura necessária"""
    
    environment = get_environment()
    
    if environment in ['external', 'production']:
        # Para EasyPanel, testar a conexão primeiro
        return test_database_connection()
    else:
        # Para SQLite local
        os.makedirs('instance', exist_ok=True)
        return True

def fix_import_compatibility():
    """Corrige problemas de compatibilidade de importação"""
    
    try:
        from urllib.parse import urlparse
        
        # Monkey patch para werkzeug se necessário
        try:
            import werkzeug.urls
            if not hasattr(werkzeug.urls, 'url_parse'):
                werkzeug.urls.url_parse = urlparse
                print("✅ Compatibilidade werkzeug.urls.url_parse corrigida")
        except ImportError:
            pass  # werkzeug não está disponível
            
    except Exception as e:
        print(f"⚠️  Aviso: Problema de compatibilidade: {e}")

def create_admin_safely(app):
    """Cria usuário admin de forma segura"""
    
    try:
        with app.app_context():
            from app import db
            from app.models.user import User
            
            print("🔧 Verificando estrutura do banco...")
            
            try:
                # Tentar criar todas as tabelas
                db.create_all()
                print("✅ Estrutura do banco verificada/criada!")
                
                # Verificar se conseguimos acessar a tabela users
                existing_admin = User.query.filter_by(username='admin').first()
                
                if existing_admin:
                    print("✅ Usuário admin já existe!")
                    
                    # Garantir que tem senha
                    if not existing_admin.password_hash:
                        print("🔧 Corrigindo senha do admin...")
                        existing_admin.set_password('admin123')
                        existing_admin.perfil = 'admin'
                        existing_admin.ativo = True
                        db.session.commit()
                        print("✅ Senha corrigida!")
                        
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
                    print("✅ Usuário admin criado com sucesso!")
                
                return True
                
            except Exception as db_error:
                print(f"❌ Erro no banco de dados: {db_error}")
                return False
            
    except Exception as e:
        print(f"❌ Erro geral ao configurar admin: {e}")
        import traceback
        traceback.print_exc()
        return False

def initialize_app():
    """Inicializa a aplicação Flask"""
    
    print("🔧 Inicializando aplicação...")
    
    # Corrigir compatibilidade primeiro
    fix_import_compatibility()
    
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente detectado: {environment}")
    
    # Para EasyPanel, forçar variáveis de ambiente
    if environment == 'external':
        print("🔧 Configurando para EasyPanel...")
        
        # Definir explicitamente as variáveis para o EasyPanel
        os.environ['DB_HOST'] = 'easypanel.pontocomdesconto.com.br'
        os.environ['DB_PORT'] = '33070'
        os.environ['DB_USER'] = 'erp_admin'
        os.environ['DB_PASSWORD'] = '8de3405e496812d04fc7'
        os.environ['DB_NAME'] = 'erp'
        
        # Para MySQL também
        os.environ['MYSQL_HOST'] = 'easypanel.pontocomdesconto.com.br'
        os.environ['MYSQL_PORT'] = '33070'
        os.environ['MYSQL_USER'] = 'erp_admin'
        os.environ['MYSQL_PASSWORD'] = '8de3405e496812d04fc7'
        os.environ['MYSQL_DATABASE'] = 'erp'
    
    # Verificar banco antes de continuar
    if not ensure_database_exists():
        print("❌ Falha na configuração do banco de dados!")
        return None
    
    # Importar e criar app
    try:
        from app import create_app, db
        
        app = create_app(environment)
        
        print("✅ Aplicação Flask criada!")
        print(f"📊 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        
        # Mostrar blueprints
        blueprints = list(app.blueprints.keys())
        print(f"📋 Blueprints: {', '.join(blueprints) if blueprints else 'Nenhum'}")
        
        return app
        
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_production_server(app):
    """Executa servidor de produção - EasyPanel"""
    
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("="*60)
    print("🚀 SERVIDOR ERP - EASYPANEL")
    print("="*60)
    print(f"🌍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🗄️  Database: EasyPanel MySQL")
    print(f"👤 Admin: admin")
    print(f"🔐 Senha: admin123")
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
        import traceback
        traceback.print_exc()

def run_development_server(app):
    """Executa servidor de desenvolvimento"""
    
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    print("="*60)
    print("🚀 SERVIDOR DE DESENVOLVIMENTO")
    print("="*60)
    print(f"🔗 URL: http://localhost:{port}")
    print(f"👤 Login: admin")
    print(f"🔐 Senha: admin123")
    print("="*60)
    
    try:
        app.run(
            host=host,
            port=port,
            debug=True,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado")
    except Exception as e:
        print(f"\n❌ Erro no servidor: {e}")

def main():
    """Função principal"""
    
    print("🏢 SISTEMA ERP - CORRIGINDO À ROTA")
    print("="*50)
    
    # Inicializar aplicação
    app = initialize_app()
    if not app:
        print("❌ FALHA CRÍTICA NA INICIALIZAÇÃO!")
        return False
    
    # Configurar admin
    print("\n🔧 Configurando usuário administrador...")
    admin_ok = create_admin_safely(app)
    if not admin_ok:
        print("⚠️  Problema ao criar admin - continuando...")
    
    # Executar servidor
    environment = get_environment()
    print(f"\n🚀 Iniciando servidor ({environment})...")
    
    if environment in ['external', 'production']:
        run_production_server(app)
    else:
        run_development_server(app)
    
    return True

def create_application():
    """Factory para WSGI servers (Gunicorn, etc.)"""
    
    print("🔧 WSGI Factory - EasyPanel")
    
    # Configurar ambiente para EasyPanel
    environment = 'external'  # Forçar configuração externa
    
    # Definir variáveis de ambiente
    os.environ['DB_HOST'] = 'easypanel.pontocomdesconto.com.br'
    os.environ['DB_PORT'] = '33070'
    os.environ['DB_USER'] = 'erp_admin'
    os.environ['DB_PASSWORD'] = '8de3405e496812d04fc7'
    os.environ['DB_NAME'] = 'erp'
    
    fix_import_compatibility()
    
    try:
        from app import create_app, db
        
        print(f"🔧 Criando app WSGI com configuração: {environment}")
        
        app = create_app(environment)
        
        # Configurar banco em contexto
        with app.app_context():
            try:
                print("🔧 Configurando estrutura do banco...")
                db.create_all()
                
                from app.models.user import User
                
                admin = User.query.filter_by(username='admin').first()
                if not admin:
                    print("🔧 Criando admin via WSGI...")
                    admin = User(
                        username='admin',
                        email='admin@corrigindoarota.com.br',
                        perfil='admin',
                        ativo=True
                    )
                    admin.set_password('admin123')
                    db.session.add(admin)
                    db.session.commit()
                    print("✅ Admin criado via WSGI!")
                
            except Exception as e:
                print(f"⚠️  Problema WSGI: {e}")
        
        print("✅ Aplicação WSGI pronta!")
        return app
        
    except Exception as e:
        print(f"❌ Erro crítico WSGI: {e}")
        import traceback
        traceback.print_exc()
        raise

# Para WSGI servers
application = create_application()

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            print("\n❌ Sistema falhou!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Encerrado pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)