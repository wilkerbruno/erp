from flask import Blueprint

bp = Blueprint('planos', __name__, url_prefix='/planos')

from app.blueprints.planos import routes
