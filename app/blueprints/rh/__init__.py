from flask import Blueprint

bp = Blueprint('rh', __name__, url_prefix='/rh')

from app.blueprints.rh import routes
