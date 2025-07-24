from flask import Blueprint

bp = Blueprint('configuracoes', __name__)

from app.blueprints.configuracoes import routes
