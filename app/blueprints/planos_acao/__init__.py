from flask import Blueprint

bp = Blueprint('planos_acao', __name__, url_prefix='/planos_acao')

from app.blueprints.planos_acao import routes

