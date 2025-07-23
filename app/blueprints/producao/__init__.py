from flask import Blueprint

bp = Blueprint('producao', __name__, template_folder='templates')

from app.blueprints.producao import routes
