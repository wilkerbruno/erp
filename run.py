import os
import sys
from dotenv import load_dotenv

load_dotenv()


def setup_database():
    from app import app, db
    with app.app_context():
        db.create_all()
        from app.models.user import User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@corrigindoarota.com.br',
                perfil='admin',
                ativo=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()


def main():
    from app import app
    setup_database()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host=host, port=port, debug=debug, use_reloader=False)


from app import app as application

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
