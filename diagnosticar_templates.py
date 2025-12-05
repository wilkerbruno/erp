#!/usr/bin/env python3
"""
Script para diagnosticar problema com templates
Execute: python diagnosticar_templates.py
"""

import os
from pathlib import Path

print("="*70)
print("🔍 DIAGNÓSTICO DE TEMPLATES")
print("="*70)

# 1. Procurar arquivos
print("\n📁 Procurando arquivos...")

arquivos_procurados = [
    'gerenciar_ponto.html',
    'controle_ponto.html',
    'bater_ponto.html'
]

encontrados = []

# Procurar a partir do diretório atual
for root, dirs, files in os.walk('.'):
    for arquivo in arquivos_procurados:
        if arquivo in files:
            caminho_completo = os.path.join(root, arquivo)
            encontrados.append(caminho_completo)
            print(f"✅ Encontrado: {caminho_completo}")

if not encontrados:
    print("❌ Nenhum arquivo encontrado!")
else:
    print(f"\n📊 Total encontrado: {len(encontrados)} arquivo(s)")

# 2. Verificar estrutura esperada
print("\n" + "="*70)
print("📂 ESTRUTURA ESPERADA")
print("="*70)

estrutura_esperada = "app/templates/rh/ponto/"
print(f"\nFlask procura templates em: {estrutura_esperada}")

if os.path.exists(estrutura_esperada):
    print(f"✅ Pasta existe: {estrutura_esperada}")
    
    # Listar arquivos nesta pasta
    arquivos = os.listdir(estrutura_esperada)
    print(f"\n📋 Arquivos nesta pasta:")
    for arq in arquivos:
        caminho = os.path.join(estrutura_esperada, arq)
        if os.path.isfile(caminho):
            print(f"   - {arq}")
    
    # Verificar se os arquivos necessários estão lá
    print(f"\n🔍 Verificando arquivos necessários:")
    for arquivo in arquivos_procurados:
        caminho = os.path.join(estrutura_esperada, arquivo)
        if os.path.exists(caminho):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - NÃO ENCONTRADO")
else:
    print(f"❌ Pasta NÃO existe: {estrutura_esperada}")
    print(f"   Você precisa criar esta estrutura de pastas!")

# 3. Verificar routes.py
print("\n" + "="*70)
print("📄 VERIFICANDO ROUTES.PY")
print("="*70)

routes_path = "app/blueprints/rh/routes.py"

if os.path.exists(routes_path):
    print(f"✅ Arquivo existe: {routes_path}")
    
    with open(routes_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Procurar pelas funções
    funcoes = [
        ('gerenciar_ponto', 'gerenciar-ponto'),
        ('controle_ponto', 'controle-ponto')
    ]
    
    for funcao, rota in funcoes:
        if f"def {funcao}(" in conteudo:
            print(f"\n✅ Função encontrada: {funcao}()")
            
            # Tentar encontrar o render_template
            inicio = conteudo.find(f"def {funcao}(")
            if inicio != -1:
                # Pegar próximas 5 linhas
                trecho = conteudo[inicio:inicio+500]
                linhas = trecho.split('\n')[:5]
                
                for linha in linhas:
                    if 'render_template' in linha:
                        print(f"   Render: {linha.strip()}")
        else:
            print(f"\n❌ Função NÃO encontrada: {funcao}()")
else:
    print(f"❌ Arquivo NÃO existe: {routes_path}")

# 4. Sugestões
print("\n" + "="*70)
print("💡 SUGESTÕES")
print("="*70)

print("\n1. Se os arquivos NÃO estão em app/templates/rh/ponto/:")
print("   → Mova ou copie os arquivos para lá")

print("\n2. Se os arquivos estão em outro lugar:")
print("   → Ajuste o caminho no routes.py")

print("\n3. Se a pasta app/templates/rh/ponto/ não existe:")
print("   → Crie a estrutura de pastas")

print("\n" + "="*70)
print("✅ DIAGNÓSTICO COMPLETO")
print("="*70)