from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_database(app):
    with app.app_context():
        db.create_all()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)

    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')
    cloud_sql_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{db_user}:{db_password}@/{db_name}'
        f'?unix_socket=/cloudsql/{cloud_sql_connection_name}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    from .messages import messages as messages_blueprint
    app.register_blueprint(messages_blueprint)

    from .prediction import prediction as prediction_blueprint
    app.register_blueprint(prediction_blueprint)

    create_database(app)

    return app
