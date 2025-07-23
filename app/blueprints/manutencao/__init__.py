from flask import Blueprint

bp = Blueprint('manutencao', __name__, template_folder='templates')

from app.blueprints.manutencao import routes
