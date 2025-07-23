from flask import Blueprint

bp = Blueprint('planos_acao', __name__, template_folder='templates')

from app.blueprints.planos_acao import routes
