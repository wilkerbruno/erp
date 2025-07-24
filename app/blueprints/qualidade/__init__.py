from flask import Blueprint

bp = Blueprint('qualidade', __name__)

from app.blueprints.qualidade import routes
