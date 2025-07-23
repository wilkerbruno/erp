from flask import Blueprint

bp = Blueprint('relatorios', __name__, template_folder='templates')

from app.blueprints.relatorios import routes
