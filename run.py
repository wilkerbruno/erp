import os
import sys
from app import create_app, db
from flask_migrate import Migrate

def create_directories():
    """Cria diretórios necessários"""
    directories = ['uploads', 'logs', 'backups']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Diretório '{directory}' criado")

def init_database():
    """Inicializa o banco de dados"""
    try:
        print("🔧 Criando tabelas do banco de dados...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def create_admin_user():
    """Cria usuário administrador se não existir"""
    try:
        from app.models.user import User
        
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("ℹ️  Usuário admin já existe!")
            return True
        
        print("👤 Criando usuário administrador...")
        admin = User(
            username='admin',
            email='admin@corrigindoarota.com.br',
            perfil='admin'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Usuário admin criado com sucesso!")
        print("📧 Email: admin@corrigindoarota.com.br")
        print("🔑 Username: admin")
        print("🔐 Password: admin123")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        db.session.rollback()
        return False

def check_database_connection():
    """Verifica se a conexão com o banco está funcionando"""
    try:
        # Tentar uma query simples
        db.session.execute(db.text('SELECT 1'))
        print("✅ Conexão com banco de dados OK!")
        return True
    except Exception as e:
        print(f"❌ Erro de conexão com banco: {e}")
        return False

def get_environment():
    """Determina o ambiente de execução"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    # Se DATABASE_URL está definida e contém railway, usar config do railway
    database_url = os.getenv('DATABASE_URL', '')
    if 'railway' in database_url or 'rlwy.net' in database_url:
        return 'railway'
    
    # Se está em produção
    if env in ['production', 'prod']:
        return 'production'
    
    # Se está em teste
    if env in ['testing', 'test']:
        return 'testing'
    
    # Por padrão, development
    return 'development'

# Determinar ambiente
environment = get_environment()
print(f"🌍 Ambiente detectado: {environment}")

# Criar a aplicação
print("🚀 Iniciando ERP Corrigindo à Rota...")
print("=" * 50)

try:
    app = create_app(environment)
    migrate = Migrate(app, db)
    print(f"✅ Aplicação Flask criada com sucesso! (Ambiente: {environment})")
except Exception as e:
    print(f"❌ Erro ao criar aplicação: {e}")
    sys.exit(1)

@app.shell_context_processor
def make_shell_context():
    from app.models import (
        User, Colaborador, NaoConformidade, OrdemProducao, 
        PlanoAcao, ProjetoConsultoria, OrdemCompra, Fornecedor
    )
    return {
        'db': db, 
        'User': User, 
        'Colaborador': Colaborador,
        'NaoConformidade': NaoConformidade, 
        'OrdemProducao': OrdemProducao,
        'PlanoAcao': PlanoAcao,
        'ProjetoConsultoria': ProjetoConsultoria,
        'OrdemCompra': OrdemCompra,
        'Fornecedor': Fornecedor
    }

@app.cli.command()
def init_db():
    """Comando CLI para inicializar o banco"""
    with app.app_context():
        if init_database():
            create_admin_user()

@app.cli.command()
def test_db():
    """Comando CLI para testar conexão com banco"""
    with app.app_context():
        if check_database_connection():
            print("🎉 Teste de conexão bem-sucedido!")
        else:
            print("❌ Falha no teste de conexão!")

@app.cli.command()
def create_admin():
    """Comando CLI para criar usuário admin"""
    with app.app_context():
        create_admin_user()

@app.cli.command()
def reset_db():
    """Comando CLI para resetar o banco"""
    with app.app_context():
        print("⚠️  ATENÇÃO: Isso vai apagar todos os dados!")
        confirm = input("Digite 'CONFIRMAR' para continuar: ")
        if confirm == 'CONFIRMAR':
            db.drop_all()
            print("🗑️  Tabelas removidas")
            if init_database():
                create_admin_user()
        else:
            print("❌ Operação cancelada")

if __name__ == '__main__':
    with app.app_context():
        print("🔧 Configurando ambiente...")
        
        # Criar diretórios necessários
        create_directories()
        
        # Verificar conexão com banco
        if not check_database_connection():
            print("🔧 Tentando inicializar banco de dados...")
            if not init_database():
                print("❌ Falha ao configurar banco de dados")
                print("💡 Tente executar: python test_railway_connection.py")
                sys.exit(1)
        
        # Criar usuário admin se necessário
        create_admin_user()
        
        print("=" * 50)
        print("🎉 Sistema pronto para uso!")
        print(f"📍 Acesse: http://localhost:5000")
        print(f"🏠 Ambiente: {environment}")
        print(f"🗄️  Banco: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        print("=" * 50)
    
    # Iniciar servidor
    try:
        app.run(
            debug=(environment == 'development'), 
            host='0.0.0.0', 
            port=int(os.environ.get('PORT', 5000))
        )
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")