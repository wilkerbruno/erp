from flask import Blueprint

bp = Blueprint('producao', __name__, url_prefix='/producao')

from app.blueprints.producao import routes
