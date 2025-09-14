#!/usr/bin/env python3
"""
Script de inicialização otimizado para EasyPanel
Use este arquivo como comando de start no EasyPanel
"""

import os
import sys

# Configurar ambiente para EasyPanel
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONUNBUFFERED'] = '1'

# Configurações específicas do EasyPanel
os.environ['DB_HOST'] = 'easypanel.pontocomdesconto.com.br'
os.environ['DB_PORT'] = '33070'
os.environ['DB_USER'] = 'erp_admin'
os.environ['DB_PASSWORD'] = '8de3405e496812d04fc7'
os.environ['DB_NAME'] = 'erp'

def main():
    """Função principal"""
    
    print("🔧 ERP - INICIALIZAÇÃO EASYPANEL")
    print("="*40)
    
    # Verificar se temos todos os dados necessários
    port = os.environ.get('PORT')
    if not port:
        print("❌ Variável PORT não definida!")
        print("💡 Configure PORT nas variáveis de ambiente do EasyPanel")
        sys.exit(1)
    
    print(f"🌍 Porta: {port}")
    print(f"🗄️  Host DB: {os.environ.get('DB_HOST')}")
    print(f"🔌 Porta DB: {os.environ.get('DB_PORT')}")
    print("="*40)
    
    try:
        # Tentar usar a aplicação completa primeiro
        print("🔧 Tentando aplicação completa...")
        try:
            from run import application
            app = application
            print("✅ Aplicação completa carregada!")
            
        except Exception as complex_error:
            print(f"⚠️  Erro na aplicação completa: {complex_error}")
            print("🔧 Usando aplicação simplificada...")
            
            # Usar aplicação simplificada como fallback
            from app import app
            print("✅ Aplicação simplificada carregada!")
        
        # Executar aplicação
        print("🚀 Iniciando servidor...")
        
        app.run(
            host='0.0.0.0',
            port=int(port),
            debug=False,
            threaded=True,
            use_reloader=False
        )
        
    except ImportError as import_error:
        print(f"❌ Erro de importação: {import_error}")
        print("💡 Verifique se todos os arquivos estão presentes")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()