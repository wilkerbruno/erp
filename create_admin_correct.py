#!/usr/bin/env python3
import os
import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse

# Carregar variáveis de ambiente
load_dotenv()

def parse_mysql_url(url):
    """Parse da URL de conexão MySQL"""
    parsed = urlparse(url)
    return {
        'host': parsed.hostname,
        'user': parsed.username,
        'password': parsed.password,
        'port': parsed.port,
        'database': parsed.path.lstrip('/'),
        'charset': 'utf8mb4',
        'connect_timeout': 30,
        'read_timeout': 60,
        'write_timeout': 60,
        'autocommit': True
    }

def get_database_configs():
    """Retorna múltiplas configurações de banco com as novas credenciais"""
    
    # Configuração 1: Interna
    config_interno = {
        'host': 'divisions_bhs_erp',
        'user': 'erp_admin',
        'password': '8de3405e496812d04fc7',
        'port': 3306,
        'database': 'erp',
        'charset': 'utf8mb4',
        'connect_timeout': 30,
        'read_timeout': 60,
        'write_timeout': 60,
        'autocommit': True
    }
    
    # Configuração 2: Externa
    config_externo = {
        'host': 'easypanel.pontocomdesconto.com.br',
        'user': 'erp_admin',
        'password': '8de3405e496812d04fc7',
        'port': 33070,
        'database': 'erp',
        'charset': 'utf8mb4',
        'connect_timeout': 30,
        'read_timeout': 60,
        'write_timeout': 60,
        'autocommit': True
    }
    
    # Configuração 3: Via URL Interna
    url_interna = "mysql://erp_admin:8de3405e496812d04fc7@divisions_bhs_erp:3306/erp"
    config_url_interna = parse_mysql_url(url_interna)
    
    # Configuração 4: Via URL Externa
    url_externa = "mysql://erp_admin:8de3405e496812d04fc7@easypanel.pontocomdesconto.com.br:33070/erp"
    config_url_externa = parse_mysql_url(url_externa)
    
    return config_interno, config_externo, config_url_interna, config_url_externa

def connect_database():
    """Tenta conectar usando múltiplas configurações"""
    
    config_interno, config_externo, config_url_interna, config_url_externa = get_database_configs()
    
    configuracoes = [
        (config_interno, "interno (divisions_bhs_erp:3306)"),
        (config_externo, "externo (easypanel:33070)"),
        (config_url_interna, "URL interna"),
        (config_url_externa, "URL externa")
    ]
    
    for config, descricao in configuracoes:
        try:
            print(f"Tentando conexão {descricao}...")
            print(f"Host: {config['host']}:{config['port']}")
            print(f"User: {config['user']}")
            print(f"Database: {config['database']}")
            
            connection = pymysql.connect(**config)
            
            # Teste básico da conexão
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            
            print(f"Conexão {descricao} estabelecida com sucesso!")
            return connection, descricao
            
        except Exception as e:
            print(f"Conexão {descricao} falhou: {str(e)}")
            continue
    
    raise Exception("Não foi possível conectar ao banco de dados com nenhuma configuração")

def create_admin():
    """Configura o banco de dados e cria usuário admin"""
    
    connection = None
    cursor = None
    connection_type = None
    
    try:
        print("=== INICIANDO CONFIGURAÇÃO DO BANCO DE DADOS ===")
        connection, connection_type = connect_database()
        cursor = connection.cursor()
        
        print(f"\nConectado ao banco 'erp' via {connection_type}")
        
        # Verificar se o banco existe
        cursor.execute("SELECT DATABASE()")
        db_atual = cursor.fetchone()[0]
        print(f"Banco atual: {db_atual}")
        
        # Criar tabela de usuários
        print("\n1. Criando/verificando tabela users...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                perfil VARCHAR(20) DEFAULT 'user',
                ativo BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_username (username),
                INDEX idx_email (email),
                INDEX idx_perfil (perfil)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   Tabela users OK")
        
        # Verificar se admin existe
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_exists = cursor.fetchone()
        
        password_hash = generate_password_hash('admin123')
        current_time = datetime.now()
        
        if admin_exists:
            print("\n2. Admin existe, atualizando credenciais...")
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s, perfil = 'admin', ativo = 1, updated_at = %s
                WHERE username = 'admin'
            """, (password_hash, current_time))
            print("   Admin atualizado!")
        else:
            print("\n2. Criando usuário admin...")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, perfil, ativo, created_at)
                VALUES ('admin', 'admin@corrigindoarota.com.br', %s, 'admin', 1, %s)
            """, (password_hash, current_time))
            print("   Admin criado!")
        
        # Criar tabelas do sistema ERP
        print("\n3. Criando estrutura do sistema ERP...")
        
        # Tabela de categorias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                ativo BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_nome (nome)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   Tabela categorias OK")
        
        # Tabela de produtos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                codigo VARCHAR(50) UNIQUE,
                descricao TEXT,
                categoria_id INT,
                preco_custo DECIMAL(10,2) DEFAULT 0.00,
                preco_venda DECIMAL(10,2) DEFAULT 0.00,
                estoque_atual INT DEFAULT 0,
                estoque_minimo INT DEFAULT 0,
                ativo BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_codigo (codigo),
                INDEX idx_nome (nome),
                INDEX idx_categoria (categoria_id),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   Tabela produtos OK")
        
        # Tabela de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                email VARCHAR(120),
                telefone VARCHAR(20),
                cpf_cnpj VARCHAR(18),
                endereco TEXT,
                cidade VARCHAR(100),
                estado VARCHAR(2),
                cep VARCHAR(10),
                ativo BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_nome (nome),
                INDEX idx_cpf_cnpj (cpf_cnpj),
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   Tabela clientes OK")
        
        # Tabela de vendas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_id INT,
                user_id INT NOT NULL,
                numero_venda VARCHAR(20) UNIQUE,
                data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
                subtotal DECIMAL(10,2) DEFAULT 0.00,
                desconto DECIMAL(10,2) DEFAULT 0.00,
                total DECIMAL(10,2) DEFAULT 0.00,
                status VARCHAR(20) DEFAULT 'finalizada',
                observacoes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_numero_venda (numero_venda),
                INDEX idx_data_venda (data_venda),
                INDEX idx_status (status),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   Tabela vendas OK")
        
        # Tabela de itens da venda
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_venda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                venda_id INT NOT NULL,
                produto_id INT NOT NULL,
                quantidade INT NOT NULL,
                preco_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_venda (venda_id),
                INDEX idx_produto (produto_id),
                FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
                FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("   Tabela itens_venda OK")
        
        # Inserir algumas categorias padrão se não existirem
        cursor.execute("SELECT COUNT(*) FROM categorias")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("\n4. Inserindo categorias padrão...")
            categorias_default = [
                ('Eletrônicos', 'Produtos eletrônicos e tecnologia'),
                ('Roupas', 'Vestuário e acessórios'),
                ('Casa e Jardim', 'Produtos para casa e jardim'),
                ('Livros', 'Livros e material educativo'),
                ('Esportes', 'Artigos esportivos e fitness')
            ]
            
            for nome, desc in categorias_default:
                cursor.execute("""
                    INSERT INTO categorias (nome, descricao, created_at) 
                    VALUES (%s, %s, %s)
                """, (nome, desc, current_time))
            
            print("   Categorias inseridas!")
        else:
            print(f"\n4. Encontradas {count} categorias existentes")
        
        # Verificar estrutura criada
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\nTabelas criadas: {len(tables)}")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   - {table[0]}: {count} registros")
        
    except pymysql.Error as e:
        print(f"\nERRO MySQL: {e}")
        print(f"Código do erro: {e.args[0]}")
        return False
    except Exception as e:
        print(f"\nERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Fechar conexões
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    # Exibir informações de sucesso
    print("\n" + "="*70)
    print("BANCO DE DADOS ERP CONFIGURADO COM SUCESSO!")
    print("="*70)
    print(f"Tipo de conexão: {connection_type}")
    print("Banco: erp") 
    print("Usuário do banco: erp_admin")
    print("Usuário Admin do sistema: admin")
    print("Senha Admin: admin123")
    print("Email Admin: admin@corrigindoarota.com.br")
    print("="*70)
    
    return True

def test_connection_detailed():
    """Testa detalhadamente a conexão com o banco"""
    print("=== TESTE DETALHADO DE CONEXÃO ===")
    
    try:
        connection, connection_type = connect_database()
        cursor = connection.cursor()
        
        # Informações do servidor
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"MySQL Version: {version}")
        
        cursor.execute("SELECT USER()")
        user = cursor.fetchone()[0]
        print(f"Usuário conectado: {user}")
        
        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()[0]
        print(f"Banco atual: {database}")
        
        # Verificar privilégios
        cursor.execute("SHOW GRANTS")
        grants = cursor.fetchall()
        print("Privilégios:")
        for grant in grants:
            print(f"   - {grant[0]}")
        
        # Verificar tabelas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\nTabelas ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        connection.close()
        
        print(f"\nTeste concluído com sucesso via {connection_type}!")
        return True
        
    except Exception as e:
        print(f"Falha no teste: {e}")
        return False

if __name__ == "__main__":
    print("CONFIGURADOR DO SISTEMA ERP")
    print("="*50)
    print("Credenciais atualizadas:")
    print("- Usuário DB: erp_admin")
    print("- Banco: erp")
    print("- Host interno: divisions_bhs_erp:3306")
    print("- Host externo: easypanel.pontocomdesconto.com.br:33070")
    print("="*50)
    
    # Teste de conexão detalhado
    if test_connection_detailed():
        print("\n" + "="*50)
        # Configurar banco e criar admin
        if create_admin():
            print("\nSistema configurado com sucesso!")
            print("Agora você pode fazer login com:")
            print("- Usuário: admin")
            print("- Senha: admin123")
        else:
            print("\nFalha na configuração!")
    else:
        print("\nNão foi possível conectar ao banco!")