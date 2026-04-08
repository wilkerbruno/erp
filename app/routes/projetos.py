from flask import render_template
from flask_login import login_required
from app import app


@app.route('/projetos/')
@login_required
def projetos_index():
    return render_template('projetos/index.html')