from flask import Blueprint

bp = Blueprint('efo', __name__)

from app.blueprints.efo import routes
