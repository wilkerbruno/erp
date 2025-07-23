from flask import Blueprint

bp = Blueprint('configuracoes', __name__, template_folder='templates')

from app.blueprints.configuracoes import routes
