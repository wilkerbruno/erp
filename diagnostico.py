#!/usr/bin/env python3
"""
Script de Diagnóstico - Identifica problemas na configuração
"""

import os
import sys

print("="*70)
print("🔍 DIAGNÓSTICO DO SISTEMA DE REGISTRO DE PONTO")
print("="*70)

# 1. Verificar estrutura de arquivos
print("\n📁 1. VERIFICANDO ESTRUTURA DE ARQUIVOS...")

arquivos_esperados = [
    "app/__init__.py",
    "app/blueprints/rh/__init__.py",
    "app/blueprints/rh/routes.py",
    "app.py"
]

for arquivo in arquivos_esperados:
    if os.path.exists(arquivo):
        print(f"   ✅ {arquivo} existe")
    else:
        print(f"   ❌ {arquivo} NÃO ENCONTRADO")

# 2. Verificar conteúdo do routes.py
print("\n📝 2. VERIFICANDO ROUTES.PY...")

routes_path = "app/blueprints/rh/routes.py"
if os.path.exists(routes_path):
    with open(routes_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Verificar se tem as correções
    checks = {
        "Validação de JSON": "if not request.is_json:" in conteudo,
        "Validação de campos": "campos_obrigatorios" in conteudo,
        "Headers explícitos": "response.headers['Content-Type']" in conteudo,
        "Tratamento de erro": "import traceback" in conteudo,
        "Blueprint correto": "@bp.route" in conteudo
    }
    
    for check, presente in checks.items():
        if presente:
            print(f"   ✅ {check}")
        else:
            print(f"   ❌ {check} - AUSENTE")
else:
    print(f"   ❌ Arquivo routes.py não encontrado!")

# 3. Verificar app.py
print("\n📝 3. VERIFICANDO APP.PY...")

if os.path.exists("app.py"):
    with open("app.py", 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Verificar rotas duplicadas
    rotas_duplicadas = [
        "@app.route('/bater-ponto')",
        "@app.route('/api/registrar-ponto')",
        "@app.route('/api/ponto/hoje/<int:colaborador_id>')"
    ]
    
    tem_duplicadas = False
    for rota in rotas_duplicadas:
        if rota in app_content:
            print(f"   ⚠️  ROTA DUPLICADA ENCONTRADA: {rota}")
            tem_duplicadas = True
    
    if not tem_duplicadas:
        print(f"   ✅ Sem rotas duplicadas no app.py")
else:
    print(f"   ❌ app.py não encontrado!")

# 4. Verificar __init__.py do blueprint
print("\n📝 4. VERIFICANDO BLUEPRINT RH...")

bp_init = "app/blueprints/rh/__init__.py"
if os.path.exists(bp_init):
    with open(bp_init, 'r', encoding='utf-8') as f:
        bp_content = f.read()
    
    if "url_prefix='/rh'" in bp_content:
        print(f"   ✅ Blueprint com prefixo /rh correto")
    else:
        print(f"   ⚠️  Verificar prefixo do blueprint")
else:
    print(f"   ❌ __init__.py do blueprint não encontrado!")

# 5. Verificar app/__init__.py
print("\n📝 5. VERIFICANDO REGISTRO DE BLUEPRINTS...")

app_init = "app/__init__.py"
if os.path.exists(app_init):
    with open(app_init, 'r', encoding='utf-8') as f:
        init_content = f.read()
    
    # Contar quantas vezes o blueprint RH é registrado
    count = init_content.count("register_blueprint(rh_bp")
    
    if count == 0:
        print(f"   ❌ Blueprint RH NÃO está registrado!")
    elif count == 1:
        print(f"   ✅ Blueprint RH registrado uma vez (correto)")
    else:
        print(f"   ⚠️  Blueprint RH registrado {count} vezes (DUPLICADO!)")
else:
    print(f"   ⚠️  app/__init__.py não encontrado (pode estar em outro lugar)")

# 6. Resumo
print("\n" + "="*70)
print("📊 RESUMO DO DIAGNÓSTICO")
print("="*70)

print("\n🎯 PRÓXIMAS AÇÕES RECOMENDADAS:")
print("\n   Se encontrou rotas duplicadas no app.py:")
print("   → Remova as rotas @app.route('/bater-ponto'), etc")
print("\n   Se routes.py não tem as correções:")
print("   → Substitua pelo arquivo rh_routes_CORRIGIDO.py")
print("\n   Se blueprint está duplicado:")
print("   → Remova uma das ocorrências de register_blueprint")
print("\n   Após fazer alterações:")
print("   → Reinicie o servidor Flask")

print("\n" + "="*70)
print("✅ DIAGNÓSTICO CONCLUÍDO")
print("="*70)
print("\nCole a saída deste script ao reportar problemas.\n")