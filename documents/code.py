# app.py
from flask import Flask
from flask_restx import Api
from config import Config
from models import db
from routes.user_routes import ns as user_ns
from routes.health_routes import ns as health_ns


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Initialize API
    api = Api(app,
              version='1.0',
              title='Flask MySQL API',
              description='A modular Flask API with MySQL and Swagger documentation',
              doc='/docs/')

    # Register namespaces
    api.add_namespace(user_ns, path='/users')
    api.add_namespace(health_ns, path='/')

    # Create tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

# ===== config.py =====
import os
from datetime import timedelta


class Config:
    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://username:password@localhost/mydatabase'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# ===== models/__init__.py =====
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ===== models/user.py =====
from datetime import datetime
from models import db


class User(db.Model):
    """User model for database operations"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def create(cls, name, email, age=None):
        """Create a new user"""
        user = cls(name=name, email=email, age=age)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, **kwargs):
        """Update user attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self

    def delete(self):
        """Delete user"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID"""
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls):
        """Get all users"""
        return cls.query.all()


# ===== schemas/user_schemas.py =====
from flask_restx import fields


def get_user_schemas(api):
    """Get user schemas for API documentation"""

    user_model = api.model('User', {
        'id': fields.Integer(readonly=True, description='User ID'),
        'name': fields.String(required=True, description='User name', example='John Doe'),
        'email': fields.String(required=True, description='User email', example='john@example.com'),
        'age': fields.Integer(description='User age', example=30),
        'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
        'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
    })

    user_input = api.model('UserInput', {
        'name': fields.String(required=True, description='User name', example='John Doe'),
        'email': fields.String(required=True, description='User email', example='john@example.com'),
        'age': fields.Integer(description='User age', example=30)
    })

    user_update = api.model('UserUpdate', {
        'name': fields.String(description='User name'),
        'email': fields.String(description='User email'),
        'age': fields.Integer(description='User age')
    })

    return user_model, user_input, user_update


# ===== services/user_service.py =====
from models.user import User
from models import db


class UserService:
    """Service layer for user operations"""

    @staticmethod
    def get_all_users():
        """Get all users"""
        return User.get_all()

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return User.get_by_id(user_id)

    @staticmethod
    def create_user(data):
        """Create a new user with validation"""
        # Check if email already exists
        existing_user = User.get_by_email(data['email'])
        if existing_user:
            raise ValueError("Email already exists")

        try:
            return User.create(
                name=data['name'],
                email=data['email'],
                age=data.get('age')
            )
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    @staticmethod
    def update_user(user_id, data):
        """Update user with validation"""
        user = User.get_by_id(user_id)
        if not user:
            return None

        # Check if email is already taken by another user
        if 'email' in data:
            existing_user = User.query.filter(
                User.email == data['email'],
                User.id != user_id
            ).first()
            if existing_user:
                raise ValueError("Email already exists")

        try:
            return user.update(**data)
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error updating user: {str(e)}")

    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        user = User.get_by_id(user_id)
        if not user:
            return False

        try:
            user.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error deleting user: {str(e)}")


# ===== routes/user_routes.py =====
from flask import request
from flask_restx import Namespace, Resource
from services.user_service import UserService
from schemas.user_schemas import get_user_schemas

# Create namespace
ns = Namespace('users', description='User operations')

# Get schemas
user_model, user_input, user_update = get_user_schemas(ns)


@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        try:
            users = UserService.get_all_users()
            return [user.to_dict() for user in users]
        except Exception as e:
            ns.abort(500, f"Error retrieving users: {str(e)}")

    @ns.doc('create_user')
    @ns.expect(user_input, validate=True)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.get_json()

        if not data:
            ns.abort(400, "No data provided")

        # Validate required fields
        if not data.get('name') or not data.get('email'):
            ns.abort(400, "Name and email are required")

        try:
            user = UserService.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))
        except Exception as e:
            ns.abort(500, str(e))


@ns.route('/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'User identifier')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        try:
            user = UserService.get_user_by_id(user_id)
            if not user:
                ns.abort(404, "User not found")
            return user.to_dict()
        except Exception as e:
            ns.abort(500, f"Error retrieving user: {str(e)}")

    @ns.doc('update_user')
    @ns.expect(user_update, validate=True)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        data = request.get_json()
        if not data:
            ns.abort(400, "No data provided")

        try:
            user = UserService.update_user(user_id, data)
            if not user:
                ns.abort(404, "User not found")
            return user.to_dict()
        except ValueError as e:
            ns.abort(400, str(e))
        except Exception as e:
            ns.abort(500, str(e))

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete a user"""
        try:
            deleted = UserService.delete_user(user_id)
            if not deleted:
                ns.abort(404, "User not found")
            return '', 204
        except Exception as e:
            ns.abort(500, str(e))


# ===== routes/health_routes.py =====
from datetime import datetime
from flask_restx import Namespace, Resource

ns = Namespace('health', description='Health check operations')


@ns.route('/health')
class Health(Resource):
    @ns.doc('health_check')
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'Flask MySQL API'
        }