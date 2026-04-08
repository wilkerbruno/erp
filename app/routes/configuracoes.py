from flask import render_template
from flask_login import login_required
from app import app


@app.route('/configuracoes/')
@login_required
def configuracoes_index():
    return render_template('configuracoes/index.html')