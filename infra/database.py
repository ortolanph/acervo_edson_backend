from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
import time

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
        except Exception as e:
            print(f"Database connection attempt {i+1} failed: {e}")
            time.sleep(2)
    return False

def init_database(app, db):
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")