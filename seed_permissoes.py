"""
Script para popular permissões e roles padrão do sistema
Execute: python seed_permissoes.py
"""

from app import create_app, db
from app.models import Permissao, Role

app = create_app()

def criar_permissoes_padrao():
    """Cria permissões padrão do sistema"""
    
    permissoes = [
        # Permissões de Usuários
        {'nome': 'Visualizar Usuários', 'codigo': 'usuarios.visualizar', 'modulo': 'usuarios'},
        {'nome': 'Criar Usuários', 'codigo': 'usuarios.criar', 'modulo': 'usuarios'},
        {'nome': 'Editar Usuários', 'codigo': 'usuarios.editar', 'modulo': 'usuarios'},
        {'nome': 'Excluir Usuários', 'codigo': 'usuarios.excluir', 'modulo': 'usuarios'},
        
        # Permissões de RH
        {'nome': 'Visualizar Colaboradores', 'codigo': 'colaboradores.visualizar', 'modulo': 'rh'},
        {'nome': 'Criar Colaboradores', 'codigo': 'colaboradores.criar', 'modulo': 'rh'},
        {'nome': 'Editar Colaboradores', 'codigo': 'colaboradores.editar', 'modulo': 'rh'},
        {'nome': 'Excluir Colaboradores', 'codigo': 'colaboradores.excluir', 'modulo': 'rh'},
        {'nome': 'Gerenciar Folha de Pagamento', 'codigo': 'folha.gerenciar', 'modulo': 'rh'},
        {'nome': 'Visualizar Relatórios RH', 'codigo': 'rh.relatorios', 'modulo': 'rh'},
        
        # Permissões de Consultoria
        {'nome': 'Visualizar Projetos Consultoria', 'codigo': 'consultoria.visualizar', 'modulo': 'consultoria'},
        {'nome': 'Criar Projetos Consultoria', 'codigo': 'consultoria.criar', 'modulo': 'consultoria'},
        {'nome': 'Editar Projetos Consultoria', 'codigo': 'consultoria.editar', 'modulo': 'consultoria'},
        {'nome': 'Realizar Diagnósticos', 'codigo': 'diagnosticos.realizar', 'modulo': 'consultoria'},
        {'nome': 'Gerenciar Auditorias', 'codigo': 'auditorias.gerenciar', 'modulo': 'consultoria'},
        
        # Permissões de Projetos
        {'nome': 'Visualizar Projetos', 'codigo': 'projetos.visualizar', 'modulo': 'projetos'},
        {'nome': 'Criar Projetos', 'codigo': 'projetos.criar', 'modulo': 'projetos'},
        {'nome': 'Editar Projetos', 'codigo': 'projetos.editar', 'modulo': 'projetos'},
        {'nome': 'Excluir Projetos', 'codigo': 'projetos.excluir', 'modulo': 'projetos'},
        
        # Permissões de Permissões/Roles
        {'nome': 'Visualizar Permissões', 'codigo': 'permissoes.visualizar', 'modulo': 'sistema'},
        {'nome': 'Gerenciar Permissões', 'codigo': 'permissoes.gerenciar', 'modulo': 'sistema'},
        {'nome': 'Visualizar Roles', 'codigo': 'roles.visualizar', 'modulo': 'sistema'},
        {'nome': 'Criar Roles', 'codigo': 'roles.criar', 'modulo': 'sistema'},
        {'nome': 'Editar Roles', 'codigo': 'roles.editar', 'modulo': 'sistema'},
        {'nome': 'Gerenciar Níveis de Acesso', 'codigo': 'nivel_acesso.gerenciar', 'modulo': 'sistema'},
        
        # Permissões de Configurações
        {'nome': 'Acessar Configurações', 'codigo': 'config.acessar', 'modulo': 'sistema'},
        {'nome': 'Gerenciar Cargos', 'codigo': 'cargos.editar', 'modulo': 'rh'},
        {'nome': 'Gerenciar Departamentos', 'codigo': 'departamentos.editar', 'modulo': 'rh'},
    ]
    
    print("Criando permissões padrão...")
    for perm_data in permissoes:
        perm = Permissao.query.filter_by(codigo=perm_data['codigo']).first()
        if not perm:
            perm = Permissao(**perm_data, descricao=f"Permissão para {perm_data['nome']}")
            db.session.add(perm)
            print(f"  ✓ Criada: {perm_data['nome']}")
        else:
            print(f"  - Já existe: {perm_data['nome']}")
    
    db.session.commit()
    print("✅ Permissões criadas!
")

def criar_roles_padrao():
    """Cria roles padrão do sistema"""
    
    roles_config = [
        {
            'nome': 'Administrador',
            'codigo': 'admin',
            'descricao': 'Acesso total ao sistema',
            'nivel_hierarquico': 10,
            'permissoes': 'todas'  # Todas as permissões
        },
        {
            'nome': 'Gestor RH',
            'codigo': 'gestor_rh',
            'descricao': 'Gestão completa do módulo RH',
            'nivel_hierarquico': 8,
            'permissoes': [
                'colaboradores.visualizar', 'colaboradores.criar', 'colaboradores.editar',
                'folha.gerenciar', 'rh.relatorios', 'cargos.editar', 'departamentos.editar',
                'nivel_acesso.gerenciar'
            ]
        },
        {
            'nome': 'Analista RH',
            'codigo': 'analista_rh',
            'descricao': 'Operações de RH sem acesso à folha',
            'nivel_hierarquico': 5,
            'permissoes': [
                'colaboradores.visualizar', 'colaboradores.criar', 'colaboradores.editar',
                'rh.relatorios'
            ]
        },
        {
            'nome': 'Consultor',
            'codigo': 'consultor',
            'descricao': 'Acesso ao módulo de consultoria',
            'nivel_hierarquico': 6,
            'permissoes': [
                'consultoria.visualizar', 'consultoria.criar', 'consultoria.editar',
                'diagnosticos.realizar', 'auditorias.gerenciar'
            ]
        },
        {
            'nome': 'Gerente de Projetos',
            'codigo': 'gerente_projetos',
            'descricao': 'Gestão completa de projetos',
            'nivel_hierarquico': 7,
            'permissoes': [
                'projetos.visualizar', 'projetos.criar', 'projetos.editar', 'projetos.excluir'
            ]
        },
        {
            'nome': 'Colaborador',
            'codigo': 'colaborador',
            'descricao': 'Acesso básico ao sistema',
            'nivel_hierarquico': 1,
            'permissoes': [
                'colaboradores.visualizar'  # Apenas visualizar próprio perfil
            ]
        },
        {
            'nome': 'Auditor',
            'codigo': 'auditor',
            'descricao': 'Realiza auditorias e inspeções',
            'nivel_hierarquico': 6,
            'permissoes': [
                'auditorias.gerenciar', 'consultoria.visualizar', 'diagnosticos.realizar'
            ]
        }
    ]
    
    print("Criando roles padrão...")
    for role_data in roles_config:
        role = Role.query.filter_by(codigo=role_data['codigo']).first()
        
        if not role:
            role = Role(
                nome=role_data['nome'],
                codigo=role_data['codigo'],
                descricao=role_data['descricao'],
                nivel_hierarquico=role_data['nivel_hierarquico']
            )
            db.session.add(role)
            db.session.flush()
            
            # Atribuir permissões
            if role_data['permissoes'] == 'todas':
                permissoes = Permissao.query.all()
            else:
                permissoes = Permissao.query.filter(Permissao.codigo.in_(role_data['permissoes'])).all()
            
            role.permissoes = permissoes
            print(f"  ✓ Criado: {role_data['nome']} com {len(permissoes)} permissões")
        else:
            print(f"  - Já existe: {role_data['nome']}")
    
    db.session.commit()
    print("✅ Roles criados!
")

def main():
    """Executa seed de permissões"""
    with app.app_context():
        print("="*60)
        print("POPULANDO PERMISSÕES E ROLES DO SISTEMA")
        print("="*60 + "
")
        
        criar_permissoes_padrao()
        criar_roles_padrao()
        
        print("="*60)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print("="*60)
        
        # Estatísticas
        total_permissoes = Permissao.query.count()
        total_roles = Role.query.count()
        
        print(f"
📊 Estatísticas:")
        print(f"   • Permissões: {total_permissoes}")
        print(f"   • Roles: {total_roles}")

if __name__ == '__main__':
    main()
