from flask import render_template
from flask_login import login_required
from app import app


@app.route('/compras/')
@login_required
def compras_index():
    return render_template('compras/index.html')