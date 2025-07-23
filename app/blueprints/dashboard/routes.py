from flask import render_template
from flask_login import login_required
from app.blueprints.dashboard import bp

@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard/index.html')
