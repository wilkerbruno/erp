#!/usr/bin/env python3
"""
Script para debugar e testar todas as rotas
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_routes():
    """Testa se todas as rotas estão funcionando"""
    
    try:
        from app import create_app
        
        environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
        app = create_app(environment)
        
        with app.app_context():
            print("🔍 TESTANDO TODAS AS ROTAS")
            print("="*50)
            
            # Listar todas as rotas registradas
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'url': str(rule)
                })
            
            # Organizar por blueprint
            blueprints = {}
            for route in routes:
                blueprint = route['endpoint'].split('.')[0] if '.' in route['endpoint'] else 'main'
                if blueprint not in blueprints:
                    blueprints[blueprint] = []
                blueprints[blueprint].append(route)
            
            # Mostrar rotas por blueprint
            for blueprint, blueprint_routes in blueprints.items():
                print(f"\n📁 {blueprint.upper()}")
                print("-" * 30)
                
                for route in blueprint_routes:
                    methods = [m for m in route['methods'] if m not in ['HEAD', 'OPTIONS']]
                    print(f"  {route['url']} -> {route['endpoint']} {methods}")
            
            print("\n" + "="*50)
            print(f"✅ Total de rotas: {len(routes)}")
            print(f"✅ Total de blueprints: {len(blueprints)}")
            
            # Testar principais rotas
            test_urls = [
                '/',
                '/rh',
                '/rh/colaboradores', 
                '/qualidade',
                '/qualidade/nao-conformidades',
                '/producao',
                '/compras',
                '/planos-acao',
                '/consultoria',
                '/financeiro',
                '/manutencao',
                '/projetos',
                '/relatorios',
                '/configuracoes'
            ]
            
            print("\n🧪 TESTANDO URLS PRINCIPAIS")
            print("-" * 30)
            
            with app.test_client() as client:
                for url in test_urls:
                    try:
                        response = client.get(url, follow_redirects=True)
                        status = "✅" if response.status_code in [200, 302] else "❌"
                        print(f"  {status} {url} -> {response.status_code}")
                    except Exception as e:
                        print(f"  ❌ {url} -> ERRO: {e}")
            
            print("\n" + "="*50)
            print("🎉 TESTE DE ROTAS CONCLUÍDO!")
            
    except Exception as e:
        print(f"❌ Erro ao testar rotas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_routes()
