#!/usr/bin/env python3
"""
Script para corrigir a estrutura da tabela users
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from dotenv import load_dotenv

load_dotenv()

def get_environment():
    """Determina o ambiente de execução"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    database_url = os.getenv('DATABASE_URL', '')
    
    if 'railway' in database_url or 'rlwy.net' in database_url:
        return 'railway'
    else:
        return 'development'

def check_table_structure(app):
    """Verifica a estrutura atual da tabela users"""
    try:
        with app.app_context():
            print("🔍 Verificando estrutura da tabela 'users'...")
            
            inspector = db.inspect(db.engine)
            
            # Verificar se tabela existe
            if 'users' not in inspector.get_table_names():
                print("❌ Tabela 'users' não existe!")
                return False, []
            
            # Obter colunas existentes
            columns = inspector.get_columns('users')
            column_names = [col['name'] for col in columns]
            
            print("📋 Colunas existentes na tabela:")
            for i, col in enumerate(columns, 1):
                print(f"   {i}. {col['name']} ({col['type']})")
            
            return True, column_names
            
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {e}")
        return False, []

def fix_user_table_structure(app):
    """Corrige a estrutura da tabela users"""
    try:
        with app.app_context():
            print("🔧 Corrigindo estrutura da tabela 'users'...")
            
            # Verificar estrutura atual
            table_exists, existing_columns = check_table_structure(app)
            
            if not table_exists:
                print("📋 Tabela não existe, criando nova...")
                from app.models.user import User
                User.__table__.create(db.engine, checkfirst=True)
                print("✅ Tabela 'users' criada!")
                return True
            
            # Colunas esperadas no modelo
            expected_columns = {
                'id': 'INTEGER',
                'username': 'VARCHAR(80)',
                'email': 'VARCHAR(120)', 
                'password_hash': 'VARCHAR(255)',
                'perfil': 'VARCHAR(20)',
                'ativo': 'BOOLEAN',
                'created_at': 'DATETIME',
                'last_login': 'DATETIME'
            }
            
            # Verificar colunas faltantes
            missing_columns = []
            for col_name in expected_columns:
                if col_name not in existing_columns:
                    missing_columns.append(col_name)
            
            # Verificar colunas extras (que podem causar erro)
            extra_columns = []
            for col_name in existing_columns:
                if col_name not in expected_columns:
                    extra_columns.append(col_name)
            
            print(f"📊 Análise da tabela:")
            print(f"   ✅ Colunas corretas: {len(existing_columns) - len(missing_columns) - len(extra_columns)}")
            print(f"   ❌ Colunas faltantes: {len(missing_columns)}")
            print(f"   ⚠️  Colunas extras: {len(extra_columns)}")
            
            if missing_columns:
                print(f"📋 Colunas faltantes: {missing_columns}")
            
            if extra_columns:
                print(f"📋 Colunas extras: {extra_columns}")
            
            # Se há problemas estruturais, recriar tabela
            if missing_columns or extra_columns:
                print("🔄 Estrutura inconsistente detectada.")
                
                response = input("Deseja recriar a tabela 'users'? (s/N): ").lower()
                if response in ['s', 'sim', 'y', 'yes']:
                    return recreate_users_table(app)
                else:
                    print("⚠️  Mantendo estrutura atual. Podem ocorrer erros.")
                    return True
            
            print("✅ Estrutura da tabela está correta!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao corrigir estrutura: {e}")
        import traceback
        traceback.print_exc()
        return False

def backup_users_data(app):
    """Faz backup dos dados dos usuários"""
    try:
        with app.app_context():
            print("💾 Fazendo backup dos usuários existentes...")
            
            # Buscar usuários com SQL direto para evitar problemas do modelo
            result = db.session.execute(db.text("""
                SELECT id, username, email, password_hash, perfil, ativo, created_at, last_login
                FROM users
            """))
            
            users_backup = []
            for row in result:
                user_data = {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'password_hash': row[3],
                    'perfil': row[4] or 'user',
                    'ativo': bool(row[5]) if row[5] is not None else True,
                    'created_at': row[6],
                    'last_login': row[7]
                }
                users_backup.append(user_data)
            
            print(f"✅ Backup de {len(users_backup)} usuários realizado!")
            return users_backup
            
    except Exception as e:
        print(f"❌ Erro no backup: {e}")
        return []

def recreate_users_table(app):
    """Recria a tabela users com estrutura correta"""
    try:
        with app.app_context():
            print("🔄 Recriando tabela 'users'...")
            
            # Backup dos dados
            users_backup = backup_users_data(app)
            
            # Remover tabela antiga
            print("🗑️  Removendo tabela antiga...")
            db.session.execute(db.text('DROP TABLE IF EXISTS users'))
            db.session.commit()
            
            # Criar nova tabela
            print("🔧 Criando nova tabela...")
            from app.models.user import User
            User.__table__.create(db.engine, checkfirst=True)
            
            # Restaurar dados
            if users_backup:
                print(f"📥 Restaurando {len(users_backup)} usuários...")
                for user_data in users_backup:
                    user = User(
                        username=user_data['username'],
                        email=user_data['email'],
                        perfil=user_data['perfil'],
                        ativo=user_data['ativo'],
                        created_at=user_data['created_at'],
                        last_login=user_data['last_login']
                    )
                    # Restaurar hash da senha diretamente
                    user.password_hash = user_data['password_hash']
                    db.session.add(user)
                
                db.session.commit()
                print("✅ Dados restaurados!")
            
            print("✅ Tabela 'users' recriada com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao recriar tabela: {e}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass
        return False

def test_user_model(app):
    """Testa se o modelo User está funcionando"""
    try:
        with app.app_context():
            print("🧪 Testando modelo User...")
            
            from app.models.user import User
            
            # Tentar query simples
            user_count = User.query.count()
            print(f"✅ Query funcionando - Total de usuários: {user_count}")
            
            # Verificar admin
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"✅ Usuário admin encontrado: {admin.email}")
                
                # Testar métodos
                print(f"✅ Método check_password: {admin.check_password('admin123')}")
                print(f"✅ Método has_permission: {admin.has_permission('admin')}")
                print(f"✅ Método is_admin: {admin.is_admin()}")
                print(f"✅ Método get_display_name: {admin.get_display_name()}")
                
            return True
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 CORREÇÃO DA TABELA USERS")
    print("="*50)
    
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente: {environment}")
    
    try:
        # Criar app
        app = create_app(environment)
        print("✅ Aplicação Flask criada")
        
        # Testar conexão
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
            print("✅ Conexão com banco: OK")
        
        # Corrigir estrutura
        if not fix_user_table_structure(app):
            print("❌ Falha ao corrigir estrutura!")
            return False
        
        # Testar modelo
        if not test_user_model(app):
            print("❌ Falha no teste do modelo!")
            return False
        
        print("="*50)
        print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("💡 Agora execute: python create_admin_user.py")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()