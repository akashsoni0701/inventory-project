import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_cors import CORS

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("inventory_app")

db = SQLAlchemy()


def create_app() -> Flask:
    """
    Initialize and configure the Flask application.

    Returns:
        Flask: Configured Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)

    from app.routes import inventory, booking
    app.register_blueprint(inventory.bp)
    app.register_blueprint(booking.bp)

    logger.info("Flask application initialized successfully.")

    return app