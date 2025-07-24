from flask import Blueprint

bp = Blueprint('compras', __name__)

from app.blueprints.compras import routes
