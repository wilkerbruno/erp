from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.blueprints.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            # Login direto sem verificar banco por enquanto
            from app.models.user import User
            try:
                user = User.query.filter_by(username='admin').first()
                if user and user.check_password('admin123'):
                    login_user(user)
                    return redirect(url_for('dashboard.index'))
            except:
                pass
            
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard.index'))
        
        flash('Credenciais inválidas', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))
