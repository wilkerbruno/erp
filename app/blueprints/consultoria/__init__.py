from flask import Blueprint

bp = Blueprint('consultoria', __name__, template_folder='templates')

from app.blueprints.consultoria import routes
