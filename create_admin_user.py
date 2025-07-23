#!/usr/bin/env python3
"""
Script para criar usuário administrador no ERP Corrigindo à Rota
- Username: admin
- Password: admin123  
- Perfil: admin
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def get_environment():
    """Determina o ambiente de execução"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    database_url = os.getenv('DATABASE_URL', '')
    
    if 'railway' in database_url or 'rlwy.net' in database_url:
        return 'railway'
    elif env in ['production', 'prod']:
        return 'production'
    elif env in ['testing', 'test']:
        return 'testing'
    else:
        return 'development'

def test_database_connection(app):
    """Testa a conexão com o banco de dados"""
    try:
        with app.app_context():
            result = db.session.execute(db.text('SELECT 1')).scalar()
            return result == 1
    except Exception as e:
        print(f"❌ Erro de conexão com banco: {e}")
        return False

def check_user_table_exists(app):
    """Verifica se a tabela users existe"""
    try:
        with app.app_context():
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            return 'users' in tables
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return False

def create_user_table_if_not_exists(app):
    """Cria a tabela users se não existir"""
    try:
        with app.app_context():
            print("🔧 Verificando se tabela 'users' existe...")
            
            if not check_user_table_exists(app):
                print("📋 Tabela 'users' não encontrada. Criando...")
                
                # Importar o modelo User para registrá-lo
                from app.models.user import User
                
                # Criar apenas a tabela users
                User.__table__.create(db.engine, checkfirst=True)
                print("✅ Tabela 'users' criada com sucesso!")
            else:
                print("✅ Tabela 'users' já existe!")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar tabela users: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_admin_user(app):
    """Cria o usuário administrador"""
    try:
        with app.app_context():
            from app.models.user import User
            
            print("👤 CRIAÇÃO DO USUÁRIO ADMINISTRADOR")
            print("-" * 40)
            
            # Verificar se admin já existe
            print("🔍 Verificando se usuário 'admin' já existe...")
            existing_admin = User.query.filter_by(username='admin').first()
            
            if existing_admin:
                print("⚠️  USUÁRIO ADMIN JÁ EXISTE!")
                print(f"   📧 Email: {existing_admin.email}")
                print(f"   👑 Perfil: {existing_admin.perfil}")
                print(f"   ✅ Ativo: {'Sim' if existing_admin.ativo else 'Não'}")
                print(f"   📅 Criado em: {existing_admin.created_at.strftime('%d/%m/%Y %H:%M') if existing_admin.created_at else 'N/A'}")
                
                # Perguntar se quer atualizar
                print("\n🤔 O que deseja fazer?")
                print("1. Manter usuário existente")
                print("2. Atualizar senha do usuário existente")
                print("3. Recriar usuário (apagar e criar novo)")
                
                choice = input("Escolha uma opção (1-3) [1]: ").strip() or "1"
                
                if choice == "1":
                    print("✅ Mantendo usuário existente.")
                    print_admin_credentials()
                    return True
                
                elif choice == "2":
                    print("🔄 Atualizando senha do usuário...")
                    existing_admin.set_password('admin123')
                    existing_admin.ativo = True
                    existing_admin.perfil = 'admin'
                    db.session.commit()
                    print("✅ Senha atualizada com sucesso!")
                    print_admin_credentials()
                    return True
                
                elif choice == "3":
                    print("🗑️  Removendo usuário existente...")
                    db.session.delete(existing_admin)
                    db.session.commit()
                    print("✅ Usuário existente removido.")
                
                else:
                    print("❌ Opção inválida. Mantendo usuário existente.")
                    return True
            
            # Criar novo usuário admin
            print("🔨 Criando novo usuário administrador...")
            
            admin_user = User(
                username='admin',
                email='admin@corrigindoarota.com.br',
                perfil='admin',
                ativo=True,
                created_at=datetime.utcnow()
            )
            
            # Definir senha
            admin_user.set_password('admin123')
            
            # Adicionar ao banco
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ USUÁRIO ADMINISTRADOR CRIADO COM SUCESSO!")
            print_admin_credentials()
            
            # Verificar se foi criado corretamente
            verification = User.query.filter_by(username='admin').first()
            if verification and verification.check_password('admin123'):
                print("🔐 Verificação de senha: ✅ OK")
                print("🎯 Verificação de perfil: ✅ Admin")
                return True
            else:
                print("❌ Falha na verificação do usuário!")
                return False
            
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        import traceback
        traceback.print_exc()
        try:
            db.session.rollback()
        except:
            pass
        return False

def print_admin_credentials():
    """Imprime as credenciais do administrador"""
    print("\n" + "="*50)
    print("🔑 CREDENCIAIS DO ADMINISTRADOR")
    print("="*50)
    print("📧 Email: admin@corrigindoarota.com.br")
    print("👤 Username: admin")
    print("🔐 Password: admin123")
    print("👑 Perfil: Administrador")
    print("="*50)
    print("📍 Acesse: http://localhost:5000")
    print("="*50)

def test_admin_login(app):
    """Testa se o login do admin funciona"""
    try:
        with app.app_context():
            from app.models.user import User
            
            print("\n🧪 TESTANDO LOGIN DO ADMINISTRADOR")
            print("-" * 40)
            
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("❌ Usuário admin não encontrado!")
                return False
            
            # Testar senha
            if admin.check_password('admin123'):
                print("✅ Teste de senha: OK")
            else:
                print("❌ Teste de senha: FALHA")
                return False
            
            # Testar propriedades
            print(f"✅ Usuário ativo: {'Sim' if admin.ativo else 'Não'}")
            print(f"✅ Perfil admin: {'Sim' if admin.is_admin() else 'Não'}")
            print(f"✅ Permissões: {admin.has_permission('admin')}")
            
            print("🎉 TESTE DE LOGIN: SUCESSO!")
            return True
            
    except Exception as e:
        print(f"❌ Erro no teste de login: {e}")
        return False

def show_database_info(app):
    """Mostra informações sobre o banco de dados"""
    try:
        with app.app_context():
            print("\n📊 INFORMAÇÕES DO BANCO DE DADOS")
            print("-" * 40)
            
            # Informações de conexão
            db_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if 'sqlite' in db_url:
                print("🗄️  Tipo: SQLite (Desenvolvimento)")
            elif 'mysql' in db_url:
                print("🗄️  Tipo: MySQL (Produção)")
            elif 'postgresql' in db_url:
                print("🗄️  Tipo: PostgreSQL")
            else:
                print("🗄️  Tipo: Desconhecido")
            
            # Listar tabelas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Total de tabelas: {len(tables)}")
            
            if 'users' in tables:
                from app.models.user import User
                user_count = User.query.count()
                print(f"👥 Total de usuários: {user_count}")
            
            print("-" * 40)
            
    except Exception as e:
        print(f"⚠️  Erro ao obter informações do banco: {e}")

def main():
    """Função principal do script"""
    print("🚀 CRIADOR DE USUÁRIO ADMINISTRADOR")
    print("ERP Corrigindo à Rota")
    print("="*50)
    
    # Determinar ambiente
    environment = get_environment()
    print(f"🌍 Ambiente detectado: {environment}")
    
    # Criar aplicação Flask
    try:
        print("⚙️  Inicializando aplicação...")
        app = create_app(environment)
        print("✅ Aplicação Flask criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        return False
    
    # Testar conexão
    print("\n🔗 Testando conexão com banco de dados...")
    if not test_database_connection(app):
        print("❌ Falha na conexão! Verifique as configurações.")
        return False
    print("✅ Conexão com banco: OK")
    
    # Mostrar informações do banco
    show_database_info(app)
    
    # Criar tabela users se necessário
    print("\n📋 Verificando estrutura do banco...")
    if not create_user_table_if_not_exists(app):
        print("❌ Falha ao criar/verificar tabela users!")
        return False
    
    # Criar usuário admin
    print("\n👤 Criando usuário administrador...")
    if not create_admin_user(app):
        print("❌ Falha ao criar usuário admin!")
        return False
    
    # Testar login
    if not test_admin_login(app):
        print("❌ Falha no teste de login!")
        return False
    
    print("\n🎉 SCRIPT EXECUTADO COM SUCESSO!")
    print("💡 Agora você pode executar: python run.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ FALHA NA EXECUÇÃO DO SCRIPT!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⛔ Script cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)