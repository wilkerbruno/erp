from flask import Blueprint

bp = Blueprint('projetos', __name__, template_folder='templates')

from app.blueprints.projetos import routes
