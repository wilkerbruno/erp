#!/usr/bin/env python3
"""
Script para testar as rotas de registro de ponto
Execute este script para verificar se as rotas estão funcionando corretamente
"""

import requests
import json
from datetime import datetime

# =========================================================================
# CONFIGURAÇÃO
# =========================================================================

# Altere para o endereço do seu servidor
BASE_URL = "http://localhost:5000"  # ou "http://seu-servidor.com"

# =========================================================================
# FUNÇÕES DE TESTE
# =========================================================================

def test_route_exists(url, method="GET"):
    """Testa se uma rota existe"""
    print(f"\n🔍 Testando: {method} {url}")
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json={}, timeout=5)
        
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            print(f"   ✅ Rota acessível")
        elif response.status_code == 401:
            print(f"   ⚠️  Rota existe mas requer autenticação")
        elif response.status_code == 404:
            print(f"   ❌ Rota não encontrada (404)")
        else:
            print(f"   ⚠️  Status inesperado: {response.status_code}")
            
        # Verificar se está retornando HTML quando deveria ser JSON
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type and '/api/' in url:
            print(f"   ❌ ERRO: API retornando HTML em vez de JSON!")
            print(f"   Resposta: {response.text[:200]}")
        
        return response.status_code
        
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Erro de conexão - servidor não está rodando?")
        return None
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def test_registrar_ponto_api():
    """Testa a API de registro de ponto"""
    print(f"\n{'='*70}")
    print(f"🧪 TESTE: API de Registro de Ponto")
    print(f"{'='*70}")
    
    url = f"{BASE_URL}/rh/api/registrar-ponto"
    
    # Dados de teste
    dados_teste = {
        "colaborador_id": 1,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "horario": datetime.now().strftime("%H:%M:%S"),
        "tipo": "entrada",
        "latitude": -7.1195,
        "longitude": -34.8450,
        "localizacao_texto": "Cabedelo, PB",
        "home_office": False,
        "dispositivo": "Python Test Script"
    }
    
    print(f"\n📤 Enviando dados para: {url}")
    print(f"Dados: {json.dumps(dados_teste, indent=2)}")
    
    try:
        response = requests.post(
            url,
            json=dados_teste,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\n📥 Resposta:")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        # Verificar se é JSON
        content_type = response.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            print(f"   ✅ Resposta é JSON")
            try:
                data = response.json()
                print(f"\n📋 Conteúdo da resposta:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                if data.get('status') == 'success':
                    print(f"\n   ✅ SUCESSO: Ponto registrado!")
                else:
                    print(f"\n   ⚠️  API retornou erro: {data.get('message')}")
                    
            except json.JSONDecodeError:
                print(f"   ❌ Erro ao decodificar JSON")
                print(f"   Resposta raw: {response.text[:500]}")
        else:
            print(f"   ❌ ERRO: Resposta não é JSON!")
            print(f"   Content-Type recebido: {content_type}")
            print(f"   Resposta (primeiros 500 chars):")
            print(response.text[:500])
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Erro de conexão - servidor não está rodando?")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def test_ponto_hoje_api():
    """Testa a API de consulta de pontos de hoje"""
    print(f"\n{'='*70}")
    print(f"🧪 TESTE: API de Consulta de Pontos de Hoje")
    print(f"{'='*70}")
    
    colaborador_id = 1
    url = f"{BASE_URL}/rh/api/ponto/hoje/{colaborador_id}"
    
    print(f"\n📤 Consultando: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        print(f"\n📥 Resposta:")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        content_type = response.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            print(f"   ✅ Resposta é JSON")
            try:
                data = response.json()
                print(f"\n📋 Conteúdo da resposta:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                if data.get('status') == 'success':
                    registros = data.get('registros', [])
                    print(f"\n   ✅ SUCESSO: {len(registros)} registro(s) encontrado(s)")
                else:
                    print(f"\n   ⚠️  API retornou erro: {data.get('message')}")
                    
            except json.JSONDecodeError:
                print(f"   ❌ Erro ao decodificar JSON")
        else:
            print(f"   ❌ ERRO: Resposta não é JSON!")
            print(f"   Content-Type recebido: {content_type}")
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Erro de conexão - servidor não está rodando?")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

def run_all_tests():
    """Executa todos os testes"""
    print(f"\n{'='*70}")
    print(f"🚀 INICIANDO TESTES DE ROTAS DE PONTO")
    print(f"{'='*70}")
    print(f"Servidor: {BASE_URL}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Teste 1: Verificar se as rotas existem
    print(f"\n{'='*70}")
    print(f"📍 TESTE 1: Verificação de Rotas")
    print(f"{'='*70}")
    
    rotas_para_testar = [
        ("/rh/bater-ponto", "GET", "Página de bater ponto"),
        ("/rh/api/registrar-ponto", "POST", "API de registro"),
        ("/rh/api/ponto/hoje/1", "GET", "API de consulta"),
    ]
    
    for url, method, descricao in rotas_para_testar:
        print(f"\n🔗 {descricao}")
        test_route_exists(f"{BASE_URL}{url}", method)
    
    # Teste 2: Testar API de registro
    test_registrar_ponto_api()
    
    # Teste 3: Testar API de consulta
    test_ponto_hoje_api()
    
    # Resumo
    print(f"\n{'='*70}")
    print(f"✅ TESTES CONCLUÍDOS")
    print(f"{'='*70}")
    print(f"\n💡 Dicas:")
    print(f"   • Se você vir erros 401, significa que precisa estar logado")
    print(f"   • Se você vir erros 404, a rota não existe")
    print(f"   • Se você vir HTML quando esperava JSON, há rotas duplicadas")
    print(f"   • Se tudo estiver OK, as APIs estão funcionando!")
    print(f"\n")

# =========================================================================
# EXECUÇÃO
# =========================================================================

if __name__ == "__main__":
    print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                   TESTE DE ROTAS DE REGISTRO DE PONTO                 ║
╚═══════════════════════════════════════════════════════════════════════╝

Este script testa se as rotas de registro de ponto estão funcionando
corretamente e se estão retornando JSON em vez de HTML.

Certifique-se de que:
1. O servidor Flask está rodando
2. Você alterou BASE_URL se necessário
3. Você aplicou as correções recomendadas

""")
    
    input("Pressione ENTER para iniciar os testes...")
    
    run_all_tests()