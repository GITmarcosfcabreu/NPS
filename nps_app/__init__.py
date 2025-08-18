from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

from nps_app.settings import Config

def create_app(config_object=Config):
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    with app.app_context():
        from . import routes  # Import routes

        # Register Blueprints
        app.register_blueprint(routes.main_bp)

        from .api import api_bp
        app.register_blueprint(api_bp)

        from . import models

        # Create database models is now handled by migrations
        # db.create_all()

        return app
