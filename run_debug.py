#!/usr/bin/env python3
"""
Versão debug do run.py para ver todos os detalhes
"""

import os
import sys
from app import create_app, db

def main():
    print("🚀 EXECUTANDO EM MODO DEBUG")
    print("="*50)
    
    # Determinar ambiente
    environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
    print(f"🌍 Ambiente: {environment}")
    
    # Criar app
    try:
        app = create_app(environment)
        print("✅ App criado com sucesso!")
        
        with app.app_context():
            # Mostrar todas as rotas registradas
            print("\n📋 ROTAS REGISTRADAS:")
            print("-" * 30)
            
            for rule in app.url_map.iter_rules():
                methods = [m for m in rule.methods if m not in ['HEAD', 'OPTIONS']]
                print(f"  {rule} -> {rule.endpoint} {methods}")
            
            print(f"\n✅ Total de rotas: {len(list(app.url_map.iter_rules()))}")
            
            # Testar conexão com banco
            try:
                result = db.session.execute(db.text('SELECT 1')).scalar()
                print("✅ Banco de dados: OK")
            except Exception as e:
                print(f"⚠️  Banco de dados: {e}")
                
            # Criar admin se necessário
            try:
                from app.models.user import User
                admin = User.query.filter_by(username='admin').first()
                if admin:
                    print("✅ Usuário admin: OK")
                else:
                    print("⚠️  Usuário admin não encontrado")
            except Exception as e:
                print(f"⚠️  Erro ao verificar admin: {e}")
        
        print("\n" + "="*50)
        print("🎯 SISTEMA INICIANDO...")
        print("📍 Acesse: http://localhost:5000")
        print("🔑 Login: admin / admin123")
        print("="*50)
        
        # Iniciar servidor
        app.run(
            debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000))
        )
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()