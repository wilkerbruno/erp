from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates')

from app.blueprints.auth import routes
