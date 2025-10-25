import os
import sys
from dotenv import load_dotenv

# PATCH PARA PYTHON 3.13 + SQLAlchemy - DEVE VIR ANTES DE QUALQUER IMPORT DO SQLAlchemy
if sys.version_info >= (3, 13):
    print("🔧 Aplicando patch de compatibilidade Python 3.13 + SQLAlchemy...")
    
    # Patch para resolver problema TypingOnly
    def patch_sqlalchemy_typing():
        try:
            import sqlalchemy.util.langhelpers
            
            # Salvar a classe original
            _original_TypingOnly = sqlalchemy.util.langhelpers.TypingOnly
            
            class PatchedTypingOnly(_original_TypingOnly):
                def __init_subclass__(cls, **kwargs):
                    # Remove atributos problemáticos antes da verificação
                    problematic_attrs = {'__firstlineno__', '__static_attributes__'}
                    
                    # Criar uma cópia do __dict__ sem os atributos problemáticos
                    new_dict = {}
                    for key, value in cls.__dict__.items():
                        if key not in problematic_attrs:
                            new_dict[key] = value
                    
                    # Remover os atributos problemáticos da classe
                    for attr in problematic_attrs:
                        if hasattr(cls, attr):
                            try:
                                delattr(cls, attr)
                            except (AttributeError, TypeError):
                                pass
                    
                    super().__init_subclass__(**kwargs)
            
            # Substituir a classe original
            sqlalchemy.util.langhelpers.TypingOnly = PatchedTypingOnly
            print("✅ Patch SQLAlchemy aplicado com sucesso!")
            
        except Exception as e:
            print(f"⚠️  Erro ao aplicar patch SQLAlchemy: {e}")
    
    # Aplicar o patch antes de qualquer import
    patch_sqlalchemy_typing()

# Carrega variáveis do arquivo .env
load_dotenv()

# Prevenir múltiplas inicializações
_app_instance = None

def get_environment():
    """Determina o ambiente baseado nas variáveis disponíveis"""
    
    # FORÇAR CONFIGURAÇÃO EXTERNA para EasyPanel
    if os.getenv('PORT') or os.getenv('EASYPANEL_PROJECT_ID'):
        print("🔧 Detectado ambiente EasyPanel - usando configuração externa")
        return 'external'
    
    # Outras plataformas
    if os.getenv('RAILWAY_DB_HOST'):
        return 'railway'
    
    database_url = os.getenv('DATABASE_URL', '')
    if any(keyword in database_url for keyword in ['railway', 'rlwy.net', 'postgres', 'mysql']):
        return 'external'
    
    return 'development'

def test_database_connection():
    """Testa a conexão com o banco antes de inicializar"""
    
    try:
        from sqlalchemy import create_engine, text
        
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
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
        
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
    """Garante que o banco de dados existe"""
    
    environment = get_environment()
    
    if environment in ['external', 'production']:
        return test_database_connection()
    else:
        os.makedirs('instance', exist_ok=True)
        return True

def fix_import_compatibility():
    """Corrige problemas de compatibilidade"""
    
    try:
        from urllib.parse import urlparse
        
        try:
            import werkzeug.urls
            if not hasattr(werkzeug.urls, 'url_parse'):
                werkzeug.urls.url_parse = urlparse
                print("✅ Compatibilidade werkzeug corrigida")
        except ImportError:
            pass
            
    except Exception as e:
        print(f"⚠️  Problema de compatibilidade: {e}")

def create_admin_safely(app):
    """Cria usuário admin de forma segura"""
    
    try:
        with app.app_context():
            from app import db
            from app.models.user import User
            
            print("🔧 Verificando estrutura do banco...")
            
            try:
                db.create_all()
                print("✅ Estrutura do banco verificada!")
                
                existing_admin = User.query.filter_by(username='admin').first()
                
                if existing_admin:
                    print("✅ Usuário admin já existe!")
                    
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
                    print("✅ Usuário admin criado!")
                
                return True
                
            except Exception as db_error:
                print(f"❌ Erro no banco: {db_error}")
                return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def setup_environment_vars():
    """Configura variáveis de ambiente para EasyPanel"""
    
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

def initialize_app():
    """Inicializa a aplicação Flask"""
    
    global _app_instance
    
    # Evitar múltiplas inicializações
    if _app_instance is not None:
        return _app_instance
    
    print("🔧 Inicializando aplicação...")
    
    fix_import_compatibility()
    
    environment = get_environment()
    print(f"🌍 Ambiente detectado: {environment}")
    
    if environment == 'external':
        print("🔧 Configurando para EasyPanel...")
        setup_environment_vars()
    
    if not ensure_database_exists():
        print("❌ Falha na configuração do banco!")
        return None
    
    try:
        from app import create_app
        
        app = create_app(environment)
        
        print("✅ Aplicação Flask criada!")
        print(f"📊 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'N/A')}")
        
        blueprints = list(app.blueprints.keys())
        print(f"📋 Blueprints: {', '.join(blueprints) if blueprints else 'Nenhum'}")
        
        _app_instance = app
        return app
        
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_production_server(app):
    """Executa servidor de produção"""
    
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
    
    app = initialize_app()
    if not app:
        print("❌ FALHA NA INICIALIZAÇÃO!")
        return False
    
    print("\n🔧 Configurando administrador...")
    admin_ok = create_admin_safely(app)
    if not admin_ok:
        print("⚠️  Problema ao configurar admin - continuando...")
    
    environment = get_environment()
    print(f"\n🚀 Iniciando servidor ({environment})...")
    
    if environment in ['external', 'production']:
        run_production_server(app)
    else:
        run_development_server(app)
    
    return True

def create_application():
    """Factory para WSGI servers"""
    
    global _app_instance
    
    # Evitar recriação se já existe
    if _app_instance is not None:
        print("✅ Usando instância existente")
        return _app_instance
    
    print("🔧 WSGI Factory - EasyPanel")
    
    fix_import_compatibility()
    setup_environment_vars()
    
    environment = 'external'
    


# ===== PATCH: Flask Markup Compatibility =====
    try:
        from markupsafe import Markup
        import flask
        if not hasattr(flask, 'Markup'):
            flask.Markup = Markup
        print("✅ Patch Flask Markup aplicado!")
    except ImportError:
        print("⚠️  markupsafe não encontrado!")
    except Exception as e:
        print(f"⚠️  Erro no patch Markup: {e}")

        from app import create_app, db
            
        print(f"🔧 Criando app WSGI: {environment}")
            
        app = create_app(environment)
            
        with app.app_context():
                try:
                    print("🔧 Configurando banco via WSGI...")
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
                    _app_instance = app
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