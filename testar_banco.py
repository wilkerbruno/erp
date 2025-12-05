#!/usr/bin/env python3
"""
Script de teste - Verificar registros no banco
Execute: python testar_banco.py
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.registros_ponto import RegistroPonto
from datetime import date

print("="*70)
print("🔍 TESTANDO BANCO DE DADOS - REGISTROS DE PONTO")
print("="*70)

try:
    app = create_app('development')
    
    with app.app_context():
        hoje = date.today()
        
        # Buscar TODOS os registros
        print(f"\n📊 TODOS OS REGISTROS:")
        todos = RegistroPonto.query.all()
        print(f"   Total de registros no banco: {len(todos)}")
        
        if len(todos) > 0:
            print("\n📋 Lista de registros:")
            for r in todos:
                print(f"   ID: {r.id}")
                print(f"      Colaborador: {r.colaborador_id}")
                print(f"      Data: {r.data}")
                print(f"      Horário: {r.horario}")
                print(f"      Tipo: {r.tipo}")
                print(f"      Atraso: {r.atraso_minutos} min")
                print(f"      Home Office: {r.home_office}")
                print("-" * 60)
        
        # Buscar registros de HOJE
        print(f"\n📅 REGISTROS DE HOJE ({hoje}):")
        registros_hoje = RegistroPonto.query.filter(
            RegistroPonto.data == hoje
        ).order_by(RegistroPonto.horario.asc()).all()
        
        print(f"   Total de registros de hoje: {len(registros_hoje)}")
        
        if len(registros_hoje) > 0:
            print("\n📋 Registros de hoje:")
            for r in registros_hoje:
                print(f"   {r.horario} | {r.tipo} | Atraso: {r.atraso_minutos}min")
        else:
            print("\n⚠️  Nenhum registro encontrado para hoje!")
            print(f"   Data de hoje: {hoje}")
            print(f"   Datas no banco: {[r.data for r in todos]}")
        
        # Testar conversão to_dict()
        if len(registros_hoje) > 0:
            print(f"\n🔄 Teste de conversão to_dict():")
            teste = registros_hoje[0].to_dict()
            print(f"   {teste}")
        
        print("\n" + "="*70)
        print("✅ TESTE CONCLUÍDO")
        print("="*70)
        
        # Instruções
        print("\n💡 PRÓXIMOS PASSOS:")
        
        if len(registros_hoje) == 0:
            print("   1. Não há registros para hoje")
            print("   2. Registre um ponto em: http://localhost:5000/rh/bater-ponto")
            print("   3. Execute este script novamente")
        else:
            print("   1. Os dados ESTÃO no banco ✓")
            print("   2. Se não aparecem na tela, o problema é:")
            print("      - A função api_ponto_hoje não está correta")
            print("      - O JavaScript não está chamando a API")
            print("      - O JavaScript não está renderizando os cards")
            print("   3. Veja o console do servidor ao acessar a página")
            print("   4. Veja o console do navegador (F12)")
        
        print("")
        
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    print(traceback.format_exc())