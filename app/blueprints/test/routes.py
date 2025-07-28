from flask import render_template
from flask_login import login_required
from app.blueprints.test import bp

@bp.route('/hamburger')
@login_required
def hamburger():
    return render_template('test/hamburger.html')

@bp.route('/responsivo')
@login_required 
def responsivo():
    return render_template('test/responsivo.html')
