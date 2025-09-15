from flask import Blueprint

bp = Blueprint('reunioes', __name__, url_prefix='/reunioes')

from app.blueprints.reunioes import routes
