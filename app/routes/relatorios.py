from flask import render_template
from flask_login import login_required
from app import app


@app.route('/relatorios/')
@login_required
def relatorios_index():
    return render_template('relatorios/index.html')