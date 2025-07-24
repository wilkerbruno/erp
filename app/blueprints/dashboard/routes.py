from flask import render_template
from flask_login import login_required, current_user
from app.blueprints.dashboard import bp

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    try:
        # Renderizar template de forma super segura
        return render_template('dashboard/index.html')
    except Exception as e:
        # Fallback se der erro
        return f'''
        <h1>Dashboard - Sistema Funcionando!</h1>
        <p>Bem-vindo ao ERP!</p>
        <p>Usuário: {current_user.username if current_user.is_authenticated else "Desconhecido"}</p>
        <p><a href="/rh">RH</a> | <a href="/qualidade">Qualidade</a> | <a href="/auth/logout">Sair</a></p>
        <p>Erro: {str(e)}</p>
        '''
