from flask import Blueprint

bp = Blueprint('financeiro', __name__)

from app.blueprints.financeiro import routes
