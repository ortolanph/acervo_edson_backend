import logging
import os

from flask import Flask

from infra import general_bp
from infra.config import config
from infra.database import wait_for_db, init_database, db
from obras.musicais.controllers import instrumentos_bp, composicoes_bp

logging.basicConfig(
    level=logging.INFO,
)


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['Access-Control-Allow-Origin'] = '*'
    app.config['Access-Control-Allow-Credentials'] = 'true'
    app.config.from_object(config[config_name])

    db.init_app(app)

    app.register_blueprint(general_bp)
    app.register_blueprint(instrumentos_bp)
    app.register_blueprint(composicoes_bp)

    return app


def main():
    """Main application entry point"""
    # Get configuration environment
    config_name = os.getenv('FLASK_ENV', 'default')

    # Create Flask app
    app = create_app(config_name)

    # Wait for database to be ready
    if wait_for_db(app.config['DATABASE_URL']):
        # Initialize database tables
        init_database(app, db)

        # Run the application
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG']
        )
    else:
        print("Failed to connect to database. Exiting...")
        exit(1)


if __name__ == '__main__':
    main()
