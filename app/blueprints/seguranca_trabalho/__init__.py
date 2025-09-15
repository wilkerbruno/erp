from flask import Blueprint

bp = Blueprint('seguranca_trabalho', __name__, url_prefix='/seguranca-trabalho')

from app.blueprints.seguranca_trabalho import routes
