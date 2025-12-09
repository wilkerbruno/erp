from flask import Blueprint

bp = Blueprint('qualidade', __name__, url_prefix='/qualidade')

from app.blueprints.qualidade import routes
