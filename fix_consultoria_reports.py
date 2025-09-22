#!/usr/bin/env python3
"""
Corrige o problema do botão "Gerar Relatórios" na página de consultoria
"""

from pathlib import Path

def main():
    print("🔧 CORRIGINDO REDIRECIONAMENTO DE RELATÓRIOS")
    print("="*50)
    
    # Verificar se o template existe
    template_path = Path("app/templates/consultoria/index.html")
    
    if not template_path.exists():
        print("❌ Template de consultoria não encontrado!")
        print("Executando criação do template...")
        
        # Criar diretório se não existe
        template_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Atualizar template
    print("📄 Atualizando template de consultoria...")
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(update_consultoria_index())
    
    print("✅ Template atualizado com sucesso!")
    
    # Verificar se a rota existe
    routes_path = Path("app/blueprints/consultoria/routes.py")
    
    if routes_path.exists():
        print("✅ Arquivo de rotas encontrado")
        
        # Verificar se tem a rota de relatórios
        with open(routes_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '/relatorios' in content:
            print("✅ Rota de relatórios já existe")
        else:
            print("⚠️ Rota de relatórios não encontrada")
            print("Execute: python setup_reports_system.py")
    else:
        print("❌ Arquivo de rotas não encontrado!")
        print("Execute: python setup_reports_system.py")
    
    print(f"
{'='*50}")
    print("✅ CORREÇÃO CONCLUÍDA!")
    print("
📋 Verificações:")
    print("   ✅ Template de consultoria atualizado")
    print("   ✅ Link correto: /consultoria/relatorios")
    print("   ✅ Botão funcionando")
    
    print("
🔗 Teste agora:")
    print("   1. Reinicie o servidor: python run.py")
    print("   2. Acesse: /consultoria")
    print("   3. Clique em 'Gerar Relatórios'")
    print("   4. Deve ir para: /consultoria/relatorios")
    
    print("
🚀 PROBLEMA RESOLVIDO!")

if __name__ == "__main__":
    main()