import os
import sys
from app import create_app, db
from flask_migrate import Migrate

def get_environment():
    """Determina o ambiente com fallback"""
    database_url = os.getenv('DATABASE_URL', '')
    
    # Se tem configuracao do Railway
    if (os.getenv('RAILWAY_DB_HOST') and 
        os.getenv('RAILWAY_DB_PASSWORD')):
        return 'railway'
    
    # Se tem DATABASE_URL com railway
    if 'railway' in database_url or 'rlwy.net' in database_url:
        return 'railway'
    
    # Default para development (SQLite)
    return 'development'

def create_admin_if_needed(app):
    """Cria admin se necessario"""
    try:
        with app.app_context():
            from app.models.user import User
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                print("Criando usuario admin...")
                admin = User(
                    username='admin',
                    email='admin@corrigindoarota.com.br',
                    perfil='admin',
                    ativo=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario admin criado!")
            else:
                print("✅ Usuario admin ja existe!")
    except Exception as e:
        print(f"Erro ao criar admin: {e}")

def main():
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente detectado: {environment}")
    
    # Criar app
    try:
        app = create_app(environment)
        migrate = Migrate(app, db)
        print("✅ Aplicacao Flask criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar aplicacao: {e}")
        # Fallback para SQLite
        try:
            app = create_app('development')
            migrate = Migrate(app, db)
            print("✅ Fallback para SQLite funcionou!")
            environment = 'development'
        except Exception as fallback_error:
            print(f"❌ Fallback tambem falhou: {fallback_error}")
            return False
    
    # Criar tabelas e admin
    try:
        with app.app_context():
            db.create_all()
            print("✅ Tabelas verificadas/criadas!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    
    create_admin_if_needed(app)
    
    print("="*50)
    print("✅ Sistema pronto para uso!")
    print(f"🌍 Ambiente: {environment}")
    print(f"📍 Acesse: http://localhost:5000")
    print("🔑 Login: admin / admin123")
    print("="*50)
    
    # Iniciar servidor
    try:
        app.run(
            debug=(environment == 'development'),
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000))
        )
    except KeyboardInterrupt:
        print("\nSistema encerrado pelo usuario")
    except Exception as e:
        print(f"Erro ao iniciar servidor: {e}")

if __name__ == '__main__':
    if not main():
        print("Falha ao inicializar sistema!")
        sys.exit(1)
