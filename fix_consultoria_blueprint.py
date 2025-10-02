#!/usr/bin/env python3
"""
Corrige o erro de blueprint não definido no routes.py da consultoria
"""

from pathlib import Path

def fix_routes_file():
    """Corrige o arquivo routes.py com o blueprint correto"""
    
    route_file = Path("app/blueprints/consultoria/routes.py")
    
    if not route_file.exists():
        print("❌ Arquivo routes.py não encontrado!")
        return False
    
    # Ler conteúdo
    with open(route_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📝 Analisando arquivo routes.py...")
    
    # Verificar se o blueprint está definido
    if 'Blueprint' in content:
        # Extrair o nome do blueprint
        lines = content.split('\n')
        blueprint_name = None
        
        for line in lines:
            if 'Blueprint(' in line and '=' in line:
                # Exemplo: bp = Blueprint('consultoria', __name__)
                parts = line.split('=')
                if len(parts) >= 2:
                    blueprint_name = parts[0].strip()
                    print(f"✅ Blueprint encontrado: {blueprint_name}")
                    break
        
        if not blueprint_name:
            print("⚠️  Não foi possível identificar o nome do blueprint")
            print("   Vou usar 'bp' como padrão")
            blueprint_name = 'bp'
        
        # Substituir @consultoria por @{blueprint_name}
        content = content.replace('@consultoria.route(', f'@{blueprint_name}.route(')
        content = content.replace('@consultoria.errorhandler(', f'@{blueprint_name}.errorhandler(')
        
        print(f"✅ Substituindo @consultoria por @{blueprint_name}")
        
    else:
        # Blueprint não definido, vamos adicionar
        print("⚠️  Blueprint não encontrado, adicionando definição...")
        
        blueprint_definition = '''from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user

bp = Blueprint('consultoria', __name__)

'''
        
        # Adicionar no início do arquivo
        content = blueprint_definition + content
        
        # Substituir @consultoria por @bp
        content = content.replace('@consultoria.route(', '@bp.route(')
        content = content.replace('@consultoria.errorhandler(', '@bp.errorhandler(')
        
        print("✅ Blueprint 'bp' adicionado ao arquivo")
    
    # Salvar arquivo corrigido
    with open(route_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Arquivo routes.py corrigido!")
    return True

def verify_init_file():
    """Verifica e corrige o __init__.py se necessário"""
    
    init_file = Path("app/blueprints/consultoria/__init__.py")
    
    if not init_file.exists():
        print("⚠️  Criando __init__.py...")
        
        init_content = '''"""
Módulo de Consultoria
"""

from flask import Blueprint

bp = Blueprint('consultoria', __name__, url_prefix='/consultoria')

from app.blueprints.consultoria import routes
'''
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        print("✅ __init__.py criado!")
        return True
    
    # Ler conteúdo existente
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se importa o blueprint corretamente
    if 'from app.blueprints.consultoria import routes' not in content:
        print("⚠️  Adicionando import de routes ao __init__.py...")
        
        if not content.endswith('\n'):
            content += '\n'
        
        content += '\nfrom app.blueprints.consultoria import routes\n'
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Import de routes adicionado!")
    
    print("✅ __init__.py verificado!")
    return True

def show_file_preview():
    """Mostra preview do arquivo corrigido"""
    
    route_file = Path("app/blueprints/consultoria/routes.py")
    
    if route_file.exists():
        with open(route_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print("\n📄 Preview das primeiras 30 linhas do routes.py:")
        print("="*60)
        for i, line in enumerate(lines[:30], 1):
            print(f"{i:3d}: {line.rstrip()}")
        print("="*60)

def main():
    """Executa a correção"""
    
    print("🔧 CORRIGINDO ERRO DE BLUEPRINT NA CONSULTORIA")
    print("="*50)
    
    try:
        # 1. Verificar e corrigir __init__.py
        print("\n1. 🔍 Verificando __init__.py...")
        verify_init_file()
        
        # 2. Corrigir routes.py
        print("\n2. 🔧 Corrigindo routes.py...")
        if not fix_routes_file():
            print("❌ Erro ao corrigir routes.py")
            return False
        
        # 3. Mostrar preview
        print("\n3. 👀 Preview do arquivo corrigido...")
        show_file_preview()
        
        print(f"\n{'='*50}")
        print("✅ CORREÇÃO CONCLUÍDA!")
        
        print("\n📋 O que foi corrigido:")
        print("   • Blueprint definido corretamente")
        print("   • Rotas usando o nome correto do blueprint")
        print("   • __init__.py verificado/corrigido")
        
        print("\n🚀 Próximos passos:")
        print("   1. Reinicie o servidor Flask")
        print("   2. Teste acessando /consultoria")
        
        print("\n💡 Dica:")
        print("   Se ainda houver erro, verifique se todas as rotas")
        print("   estão usando @bp.route() e não @consultoria.route()")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🎉 CORREÇÃO BEM-SUCEDIDA!")
    else:
        print(f"\n💥 ERRO NA CORREÇÃO")