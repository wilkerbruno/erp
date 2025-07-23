from flask import Blueprint

bp = Blueprint('compras', __name__, template_folder='templates')

from app.blueprints.compras import routes
