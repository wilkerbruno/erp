#!/usr/bin/env python3
"""
Debug completo do sistema ERP
"""
import os
import sys
import traceback
from datetime import datetime

def log_message(message, level="INFO"):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def test_environment():
    """Testa variáveis de ambiente"""
    log_message("VERIFICANDO AMBIENTE", "DEBUG")
    
    env_vars = [
        'DATABASE_URL', 'FLASK_ENV', 'MYSQL_HOST', 'MYSQL_PORT',
        'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'NÃO DEFINIDA')
        if 'PASSWORD' in var:
            value = '***' if value != 'NÃO DEFINIDA' else 'NÃO DEFINIDA'
        log_message(f"{var}: {value}")

def test_database_raw():
    """Testa conexão direta com MySQL"""
    log_message("TESTANDO CONEXÃO DIRETA MYSQL", "DEBUG")
    
    # Tenta diferentes combinações de host
    hosts_to_try = [
        ('divisions_bhs_erp_bd', 3306),
        ('easypanel.pontocomdesconto.com.br', 33070),
        ('localhost', 3306),
        ('127.0.0.1', 3306)
    ]
    
    for host, port in hosts_to_try:
        try:
            log_message(f"Tentando conectar em {host}:{port}...")
            
            import pymysql
            connection = pymysql.connect(
                host=host,
                port=port,
                user='erp_admin',
                password='8de3405e496812d04fc7',
                database='erp',
                charset='utf8mb4',
                connect_timeout=5
            )
            
            log_message(f"✅ SUCESSO em {host}:{port}", "SUCCESS")
            
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            log_message(f"MySQL Version: {version}")
            
            # Verifica estrutura
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            log_message(f"Tabelas encontradas ({len(tables)}): {tables}")
            
            if 'users' in tables:
                cursor.execute("DESCRIBE users")
                columns = cursor.fetchall()
                log_message("Estrutura da tabela users:")
                for col in columns:
                    log_message(f"  - {col[0]} ({col[1]})")
                
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]
                log_message(f"Total de usuários: {count}")
                
                if count > 0:
                    cursor.execute("SELECT username, email, active FROM users LIMIT 3")
                    users = cursor.fetchall()
                    log_message("Usuários:")
                    for user in users:
                        log_message(f"  - {user[0]} ({user[1]}) - Ativo: {user[2]}")
            
            connection.close()
            return True
            
        except Exception as e:
            log_message(f"❌ FALHA em {host}:{port} - {e}", "ERROR")
    
    return False

def test_flask_sqlalchemy():
    """Testa Flask-SQLAlchemy"""
    log_message("TESTANDO FLASK-SQLALCHEMY", "DEBUG")
    
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        app = Flask(__name__)
        
        # Tenta diferentes URLs de conexão
        database_urls = [
            'mysql+pymysql://erp_admin:8de3405e496812d04fc7@divisions_bhs_erp_bd:3306/erp',
            'mysql+pymysql://erp_admin:8de3405e496812d04fc7@easypanel.pontocomdesconto.com.br:33070/erp',
            os.environ.get('DATABASE_URL', '')
        ]
        
        for db_url in database_urls:
            if not db_url:
                continue
                
            try:
                log_message(f"Testando URL: {db_url.replace('8de3405e496812d04fc7', '***')}")
                
                app.config['SQLALCHEMY_DATABASE_URI'] = db_url
                app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
                
                db = SQLAlchemy(app)
                
                with app.app_context():
                    result = db.engine.execute("SELECT 1").scalar()
                    log_message(f"✅ SQLAlchemy OK: {result}", "SUCCESS")
                    return True
                    
            except Exception as e:
                log_message(f"❌ SQLAlchemy falhou: {e}", "ERROR")
        
        return False
        
    except Exception as e:
        log_message(f"❌ Erro Flask: {e}", "ERROR")
        return False

def create_test_user():
    """Cria usuário de teste"""
    log_message("CRIANDO USUÁRIO DE TESTE", "DEBUG")
    
    try:
        import pymysql
        from werkzeug.security import generate_password_hash
        
        connection = pymysql.connect(
            host='divisions_bhs_erp_bd',  # Assumindo que a conexão funciona
            port=3306,
            user='erp_admin',
            password='8de3405e496812d04fc7',
            database='erp',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Remove usuário teste se existir
        cursor.execute("DELETE FROM users WHERE username = 'teste'")
        
        # Cria usuário teste
        password_hash = generate_password_hash('123456')
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, active, created_at)
            VALUES ('teste', 'teste@teste.com', %s, 1, NOW())
        """, (password_hash,))
        
        connection.commit()
        log_message("✅ Usuário 'teste' criado (senha: 123456)", "SUCCESS")
        
        # Verifica se foi criado
        cursor.execute("SELECT id, username, email FROM users WHERE username = 'teste'")
        user = cursor.fetchone()
        if user:
            log_message(f"Usuário criado: ID={user[0]}, Username={user[1]}, Email={user[2]}")
        
        connection.close()
        return True
        
    except Exception as e:
        log_message(f"❌ Erro ao criar usuário: {e}", "ERROR")
        return False

def test_login_logic():
    """Testa lógica de login"""
    log_message("TESTANDO LÓGICA DE LOGIN", "DEBUG")
    
    try:
        from werkzeug.security import check_password_hash, generate_password_hash
        
        # Testa hash de senha
        test_password = 'admin123'
        hash1 = generate_password_hash(test_password)
        hash2 = generate_password_hash(test_password)
        
        log_message(f"Hash 1: {hash1[:50]}...")
        log_message(f"Hash 2: {hash2[:50]}...")
        log_message(f"Hashes diferentes (correto): {hash1 != hash2}")
        
        # Testa verificação
        check1 = check_password_hash(hash1, test_password)
        check2 = check_password_hash(hash1, 'senha_errada')
        
        log_message(f"Verificação senha correta: {check1}")
        log_message(f"Verificação senha errada: {check2}")
        
        if check1 and not check2:
            log_message("✅ Lógica de hash OK", "SUCCESS")
            return True
        else:
            log_message("❌ Problema na lógica de hash", "ERROR")
            return False
            
    except Exception as e:
        log_message(f"❌ Erro na lógica de login: {e}", "ERROR")
        return False

def test_flask_session():
    """Testa sessões Flask"""
    log_message("TESTANDO SESSÕES FLASK", "DEBUG")
    
    try:
        from flask import Flask
        
        app = Flask(__name__)
        app.secret_key = 'test-secret-key'
        
        with app.test_request_context():
            from flask import session
            
            # Testa sessão
            session['test'] = 'valor_teste'
            valor = session.get('test')
            
            log_message(f"Valor da sessão: {valor}")
            
            if valor == 'valor_teste':
                log_message("✅ Sessões Flask OK", "SUCCESS")
                return True
            else:
                log_message("❌ Problema nas sessões", "ERROR")
                return False
                
    except Exception as e:
        log_message(f"❌ Erro nas sessões: {e}", "ERROR")
        return False

def main():
    """Executa todos os testes"""
    log_message("INICIANDO DIAGNÓSTICO COMPLETO", "INFO")
    print("=" * 80)
    
    tests = [
        ("Ambiente", test_environment),
        ("Database Raw", test_database_raw),
        ("Flask-SQLAlchemy", test_flask_sqlalchemy),
        ("Login Logic", test_login_logic),
        ("Flask Sessions", test_flask_session),
        ("Create Test User", create_test_user)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        log_message(f"EXECUTANDO: {test_name}", "INFO")
        try:
            result = test_func()
            results[test_name] = result
            log_message(f"RESULTADO {test_name}: {'✅ OK' if result else '❌ FALHA'}", "INFO")
        except Exception as e:
            results[test_name] = False
            log_message(f"ERRO em {test_name}: {e}", "ERROR")
            traceback.print_exc()
        
        print("-" * 40)
    
    # Resumo
    print("=" * 80)
    log_message("RESUMO DOS TESTES", "INFO")
    
    for test_name, result in results.items():
        status = "✅ OK" if result else "❌ FALHA"
        log_message(f"{test_name}: {status}")
    
    total_ok = sum(results.values())
    log_message(f"TOTAL: {total_ok}/{len(results)} testes passaram", "INFO")

if __name__ == "__main__":
    main()