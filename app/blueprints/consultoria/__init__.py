from flask import Blueprint

bp = Blueprint('consultoria', __name__)

from app.blueprints.consultoria import routes
