#!/usr/bin/env python3
"""
Script para debuggar erro 500 após login
"""

import os
import sys
from app import create_app, db

def debug_500_error():
    """Debug do erro 500"""
    print("🔍 DEBUGANDO ERRO 500")
    print("="*50)
    
    try:
        environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
        app = create_app(environment)
        
        # Habilitar debug detalhado
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        
        with app.app_context():
            print("✅ App context criado")
            
            # Testar se consegue carregar o dashboard
            try:
                from app.blueprints.dashboard import bp
                print("✅ Blueprint dashboard importado")
            except Exception as e:
                print(f"❌ Erro ao importar dashboard blueprint: {e}")
                return
            
            # Testar template
            try:
                from flask import render_template
                # Tentar renderizar o template
                html = render_template('dashboard/index.html')
                print("✅ Template dashboard renderizado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao renderizar template dashboard: {e}")
                print("Erro detalhado:")
                import traceback
                traceback.print_exc()
                return
            
            # Testar usuário
            try:
                from app.models.user import User
                admin = User.query.filter_by(username='admin').first()
                if admin:
                    print(f"✅ Usuário admin encontrado: {admin.username}")
                    print(f"   - Display name: {admin.get_display_name()}")
                    print(f"   - Perfil: {admin.get_perfil_display()}")
                else:
                    print("❌ Usuário admin não encontrado")
            except Exception as e:
                print(f"❌ Erro ao acessar modelo User: {e}")
                import traceback
                traceback.print_exc()
        
        print("="*50)
        print("🎯 TESTE COMPLETO - verifique os erros acima")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_500_error()