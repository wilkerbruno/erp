from flask import Blueprint

bp = Blueprint('gestao_vista', __name__, url_prefix='/gestao-vista')

from app.blueprints.gestao_vista import routes
