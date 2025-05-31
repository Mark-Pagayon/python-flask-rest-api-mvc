import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

basedir = pathlib.Path(__file__).parent.resolve()

connex_app = connexion.FlaskApp(__name__, specification_dir=basedir)
app = connex_app.app

# Defaults to normal DB; will be overridden in tests
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'app.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# CONFIGURATION FOR TESTING, USES IN MEMORY DATABASE INSTEAD OF THE DEFAULT

def init_test_config(flask_app):
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["JWT_SECRET_KEY"] = "test-secret"

def create_test_app():
    import routes.notes_bp, routes.users_bp, routes.auth_bp, routes.activity_log_bp

    connex_app = connexion.FlaskApp(__name__, specification_dir=basedir)
    app = connex_app.app

    # Configure app for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test-secret"

    # Re-initialize with the correct app
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)  

    app.register_blueprint(routes.users_bp.users_bp, url_prefix='/users')
    app.register_blueprint(routes.notes_bp.notes_bp, url_prefix='/notes')
    app.register_blueprint(routes.auth_bp.auth_bp, url_prefix='/auth')
    app.register_blueprint(routes.activity_log_bp.activity_logs_bp, url_prefix='/activity-logs')

    return app