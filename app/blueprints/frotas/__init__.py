from flask import Blueprint

bp = Blueprint('frotas', __name__, url_prefix='/frotas')

from app.blueprints.frotas import routes
