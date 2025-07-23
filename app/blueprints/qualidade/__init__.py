from flask import Blueprint

bp = Blueprint('qualidade', __name__, template_folder='templates')

from app.blueprints.qualidade import routes
