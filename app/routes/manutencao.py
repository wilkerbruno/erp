from flask import render_template
from flask_login import login_required
from app import app


@app.route('/manutencao/')
@login_required
def manutencao_index():
    return render_template('manutencao/index.html')