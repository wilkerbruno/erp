import pymysql

try:
    connection = pymysql.connect(
        host='easypanel.pontocomdesconto.com.br',
        port=33070,
        user='erp_admin',
        password='8de3405e496812d04fc7',
        database='erp',
        charset='utf8mb4'
    )
    print("✅ Conexão com MySQL bem-sucedida!")
    connection.close()
except Exception as e:
    print(f"❌ Erro na conexão: {e}")