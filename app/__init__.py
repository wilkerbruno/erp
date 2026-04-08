import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config as config_dict

_base = os.path.dirname(os.path.abspath(__file__))
_env = os.getenv('FLASK_ENV', 'development')
if os.getenv('PORT') or os.getenv('EASYPANEL_PROJECT_ID'):
    _env = 'production'

app = Flask(
    __name__,
    template_folder=os.path.join(_base, 'templates'),
    static_folder=os.path.join(_base, 'static')
)
app.config.from_object(config_dict.get(_env, config_dict['development']))

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Faca login para acessar esta pagina.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


from app.routes import register_all_routes
register_all_routes()
