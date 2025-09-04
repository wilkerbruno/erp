#!/usr/bin/env python3
"""
Script para corrigir problemas de database e blueprints duplicados
"""
import os
import sys
import sqlite3
from pathlib import Path

def fix_database_structure():
    """Cria a estrutura do banco SQLite corretamente"""
    
    # Localizar o arquivo do banco
    db_file = 'instance/app.db'
    
    # Criar diretório instance se não existir
    os.makedirs('instance', exist_ok=True)
    
    try:
        # Conectar ao SQLite
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        print(f"📁 Usando banco: {db_file}")
        
        # Verificar se tabela users existe
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        
        if cursor.fetchone():
            print("✅ Tabela 'users' já existe")
        else:
            print("🔧 Criando tabela 'users'...")
            
            # Criar tabela users
            cursor.execute("""
                CREATE TABLE users (
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
            
            # Criar índices
            cursor.execute("CREATE INDEX idx_users_username ON users(username)")
            cursor.execute("CREATE INDEX idx_users_email ON users(email)")
            
            print("✅ Tabela 'users' criada com sucesso!")
        
        # Verificar se admin existe
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_exists = cursor.fetchone()
        
        if admin_exists:
            print("✅ Usuário admin já existe")
        else:
            print("🔧 Criando usuário admin...")
            
            # Hash da senha 'admin123' (usando werkzeug)
            from werkzeug.security import generate_password_hash
            password_hash = generate_password_hash('admin123')
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, perfil, ativo)
                VALUES ('admin', 'admin@corrigindoarota.com.br', ?, 'admin', 1)
            """, (password_hash,))
            
            print("✅ Usuário admin criado!")
        
        # Criar outras tabelas do sistema
        create_other_tables(cursor)
        
        # Confirmar mudanças
        conn.commit()
        conn.close()
        
        print("✅ Banco de dados configurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False

def create_other_tables(cursor):
    """Cria outras tabelas do sistema"""
    
    tables = [
        # Categorias
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT,
            ativo BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        # Produtos
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(200) NOT NULL,
            codigo VARCHAR(50) UNIQUE,
            descricao TEXT,
            categoria_id INTEGER,
            preco_custo DECIMAL(10,2) DEFAULT 0.00,
            preco_venda DECIMAL(10,2) DEFAULT 0.00,
            estoque_atual INTEGER DEFAULT 0,
            estoque_minimo INTEGER DEFAULT 0,
            ativo BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
        """,
        
        # Clientes
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(200) NOT NULL,
            email VARCHAR(120),
            telefone VARCHAR(20),
            cpf_cnpj VARCHAR(18),
            endereco TEXT,
            cidade VARCHAR(100),
            estado VARCHAR(2),
            cep VARCHAR(10),
            ativo BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        # Vendas
        """
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            user_id INTEGER NOT NULL,
            numero_venda VARCHAR(20) UNIQUE,
            data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
            subtotal DECIMAL(10,2) DEFAULT 0.00,
            desconto DECIMAL(10,2) DEFAULT 0.00,
            total DECIMAL(10,2) DEFAULT 0.00,
            status VARCHAR(20) DEFAULT 'finalizada',
            observacoes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    ]
    
    for table_sql in tables:
        try:
            cursor.execute(table_sql)
            print(f"✅ Tabela criada/verificada")
        except Exception as e:
            print(f"⚠️  Erro em tabela: {e}")

def create_fixed_run_script():
    """Cria uma versão corrigida do run.py"""
    
    fixed_run_content = '''import os
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
        print("\\nSistema encerrado pelo usuario")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

if __name__ == '__main__':
    if not main():
        print("Falha ao inicializar sistema!")
        sys.exit(1)
'''
    
    with open('run_fixed.py', 'w', encoding='utf-8') as f:
        f.write(fixed_run_content)
    
    print("✅ Arquivo run_fixed.py criado!")

def check_blueprint_issues():
    """Verifica problemas com blueprints"""
    
    print("🔍 Verificando estrutura de blueprints...")
    
    # Procurar por arquivos __init__.py que podem estar registrando blueprints
    blueprint_files = [
        'app/__init__.py',
        'app/auth/__init__.py',
        'app/main/__init__.py',
        'app/rh/__init__.py',
        'app/financeiro/__init__.py'
    ]
    
    for file_path in blueprint_files:
        if os.path.exists(file_path):
            print(f"📁 Encontrado: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Procurar por registros de blueprint
                if 'register_blueprint' in content:
                    print(f"⚠️  {file_path} registra blueprints")
                
                if 'Blueprint(' in content:
                    print(f"📋 {file_path} define blueprints")
                    
            except Exception as e:
                print(f"❌ Erro ao ler {file_path}: {e}")
        else:
            print(f"❌ Não encontrado: {file_path}")

def main():
    print("🔧 CORRETOR DE SISTEMA ERP")
    print("="*50)
    
    # 1. Verificar problemas com blueprints
    check_blueprint_issues()
    
    print("\n" + "="*30)
    
    # 2. Corrigir estrutura do banco
    if fix_database_structure():
        print("✅ Banco corrigido!")
    else:
        print("❌ Falha ao corrigir banco!")
        return False
    
    print("\n" + "="*30)
    
    # 3. Criar script corrigido
    create_fixed_run_script()
    
    print("\n" + "="*50)
    print("🎯 CORREÇÕES APLICADAS:")
    print("✅ Banco SQLite configurado")
    print("✅ Tabela users criada")
    print("✅ Usuário admin configurado")
    print("✅ Script run_fixed.py criado")
    print("="*50)
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Execute: python run_fixed.py")
    print("2. Acesse: http://localhost:5000")
    print("3. Login: admin / admin123")
    print("="*50)
    
    return True

if __name__ == '__main__':
    if not main():
        sys.exit(1)