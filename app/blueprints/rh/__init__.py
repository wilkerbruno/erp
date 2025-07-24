from flask import Blueprint

bp = Blueprint('rh', __name__)

from app.blueprints.rh import routes
