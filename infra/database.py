"""
Database
"""
import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

db = SQLAlchemy()


def wait_for_db(database_url, max_retries=30):
    """Wait for database to be ready"""
    for i in range(max_retries):
        try:
            engine = create_engine(database_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
        except AttributeError as e:
            print(f"Database connection attempt {i + 1} failed: {e}")
            time.sleep(2)
    return False


def init_database(app, database):
    """Initialize database tables"""
    with app.app_context():
        database.create_all()
        print("Database tables created successfully!")
