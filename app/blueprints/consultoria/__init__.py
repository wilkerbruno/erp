from flask import Blueprint

bp = Blueprint('consultoria', __name__, url_prefix='/consultoria')

from app.blueprints.consultoria import routes
