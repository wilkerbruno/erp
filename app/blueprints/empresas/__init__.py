from flask import Blueprint

bp = Blueprint('empresas', __name__)

from app.blueprints.empresas import routes
