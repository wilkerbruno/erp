from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import db
from app.blueprints.auth import bp
from app.forms.auth import LoginForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        try:
            from app.models.user import User
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password) and user.ativo:
                login_user(user, remember=remember_me)
                
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('dashboard.index')
                
                flash('Login realizado com sucesso!', 'success')
                return redirect(next_page)
            else:
                flash('Credenciais invalidas', 'error')
        except Exception as e:
            flash('Erro no sistema. Tente novamente.', 'error')
            print(f"Erro durante login: {e}")
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('auth.login'))
