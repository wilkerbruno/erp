from flask import Blueprint

bp = Blueprint('planos_acao', __name__)

from app.blueprints.planos_acao import routes
