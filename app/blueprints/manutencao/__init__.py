from flask import Blueprint

bp = Blueprint('manutencao', __name__)

from app.blueprints.manutencao import routes
