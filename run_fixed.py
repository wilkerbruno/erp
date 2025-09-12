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
            
            # Verificar se tabelas existem
            if not db.engine.dialect.has_table(db.engine, 'users'):
                print("🔧 Criando tabelas do banco...")
                db.create_all()
                print("✅ Tabelas criadas!")
            
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                print("🔧 Criando usuario admin...")
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
        print(f"❌ Erro ao criar admin: {e}")
        # Tentar criar via SQL direto
        try:
            print("🔧 Tentando criar via SQL direto...")
            import sqlite3
            from werkzeug.security import generate_password_hash
            
            conn = sqlite3.connect('instance/app.db')
            cursor = conn.cursor()
            
            # Verificar se admin existe
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                password_hash = generate_password_hash('admin123')
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, perfil, ativo)
                    VALUES ('admin', 'admin@corrigindoarota.com.br', ?, 'admin', 1)
                """, (password_hash,))
                conn.commit()
                print("✅ Admin criado via SQL direto!")
            
            conn.close()
        except Exception as sql_error:
            print(f"❌ Erro SQL direto: {sql_error}")

def main():
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente detectado: {environment}")
    
    # Criar app com proteção contra blueprints duplicados
    try:
        app = create_app(environment)
        
        # Verificar se já tem blueprints registrados
        existing_blueprints = list(app.blueprints.keys())
        print(f"📋 Blueprints registrados: {existing_blueprints}")
        
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
            port=int(os.environ.get('PORT', 5000)),
            use_reloader=False  # Evitar recarregamento duplo
        )
    except KeyboardInterrupt:
        print("\nSistema encerrado pelo usuario")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

if __name__ == '__main__':
    if not main():
        print("Falha ao inicializar sistema!")
        sys.exit(1)
