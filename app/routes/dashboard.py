from flask import render_template
from flask_login import login_required
from app import app


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html')
