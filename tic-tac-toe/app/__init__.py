from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from app.views import main, auth, game
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app 