from flask import Blueprint

bp = Blueprint('projetos', __name__)

from app.blueprints.projetos import routes
