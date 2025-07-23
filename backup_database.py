#!/usr/bin/env python3
"""
Script para fazer backup do banco de dados
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from dotenv import load_dotenv

load_dotenv()

def backup_database():
    """Faz backup dos dados do banco"""
    
    environment = 'railway' if 'railway' in os.getenv('DATABASE_URL', '') else 'development'
    
    print(f"💾 BACKUP DO BANCO DE DADOS")
    print("="*40)
    
    try:
        app = create_app(environment)
        
        with app.app_context():
            from app.models import User, CentroCusto, ContaFinanceira, Fornecedor, Produto, ProdutoConsultoria
            
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'environment': environment,
                'users': [],
                'centros_custo': [],
                'contas_financeiras': [],
                'fornecedores': [],
                'produtos': [],
                'produtos_consultoria': []
            }
            
            # Backup Users (sem senhas)
            for user in User.query.all():
                backup_data['users'].append({
                    'username': user.username,
                    'email': user.email,
                    'perfil': user.perfil,
                    'ativo': user.ativo
                })
            
            # Backup Centros de Custo
            for cc in CentroCusto.query.all():
                backup_data['centros_custo'].append({
                    'codigo': cc.codigo,
                    'nome': cc.nome,
                    'descricao': cc.descricao,
                    'ativo': cc.ativo
                })
            
            # Backup Contas Financeiras
            for conta in ContaFinanceira.query.all():
                backup_data['contas_financeiras'].append({
                    'codigo': conta.codigo,
                    'nome': conta.nome,
                    'tipo': conta.tipo,
                    'natureza': conta.natureza,
                    'ativo': conta.ativo
                })
            
            # Criar arquivo de backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backup_erp_{timestamp}.json"
            
            # Criar diretório de backup se não existir
            os.makedirs('backups', exist_ok=True)
            filepath = os.path.join('backups', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Backup criado: {filepath}")
            print(f"📊 Usuários: {len(backup_data['users'])}")
            print(f"📊 Centros de Custo: {len(backup_data['centros_custo'])}")
            print(f"📊 Contas: {len(backup_data['contas_financeiras'])}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro no backup: {e}")
        return False

if __name__ == "__main__":
    backup_database()