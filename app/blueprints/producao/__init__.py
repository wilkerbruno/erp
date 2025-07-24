from flask import Blueprint

bp = Blueprint('producao', __name__)

from app.blueprints.producao import routes
