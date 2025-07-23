from flask import Blueprint

bp = Blueprint('financeiro', __name__, template_folder='templates')

from app.blueprints.financeiro import routes
