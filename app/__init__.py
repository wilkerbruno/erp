from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faca login para acessar esta pagina.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    try:
        from app.blueprints.auth import bp as auth_bp
        from app.blueprints.dashboard import bp as dashboard_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(dashboard_bp, url_prefix='/')
        
        # Outros blueprints opcionais
        other_blueprints = [
            ('rh', '/rh'), ('qualidade', '/qualidade'), ('producao', '/producao'),
            ('compras', '/compras'), ('planos_acao', '/planos-acao'), 
            ('consultoria', '/consultoria'), ('financeiro', '/financeiro'),
            ('manutencao', '/manutencao'), ('projetos', '/projetos'),
            ('relatorios', '/relatorios'), ('configuracoes', '/configuracoes')
        ]
        
        for bp_name, url_prefix in other_blueprints:
            try:
                module = __import__(f'app.blueprints.{bp_name}', fromlist=['bp'])
                blueprint = getattr(module, 'bp')
                app.register_blueprint(blueprint, url_prefix=url_prefix)
            except Exception:
                pass
        
    except Exception as e:
        print(f"Erro ao registrar blueprints: {e}")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app

@login_manager.user_loader
def load_user(user_id):
    try:
        from app.models.user import User
        return User.query.get(int(user_id))
    except Exception:
        return None