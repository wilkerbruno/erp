from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse
from app import app, db
from app.forms.auth import LoginForm


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        from app.models.user import User
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data) and user.ativo:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('dashboard')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page)

        flash('Credenciais invalidas', 'error')

    return render_template('auth/login.html', form=form)


@app.route('/auth/logout')
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('login'))
