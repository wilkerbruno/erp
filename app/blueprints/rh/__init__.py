from flask import Blueprint

bp = Blueprint('rh', __name__, template_folder='templates')

from app.blueprints.rh import routes
