# Modular Flask API with MySQL and Swagger

## Project Structure

```
flask-api/
├── app.py                 # Application entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (optional)
├── models/
│   ├── __init__.py      # Database initialization
│   └── user.py          # User model
├── schemas/
│   └── user_schemas.py  # API documentation schemas
├── services/
│   └── user_service.py  # Business logic layer
└── routes/
    ├── user_routes.py   # User API endpoints
    └── health_routes.py # Health check endpoints
```

## File Creation Guide

Create the following files in your project directory:

### 1. Create the directory structure:

```bash
mkdir flask-api
cd flask-api
mkdir models schemas services routes
touch app.py config.py requirements.txt
touch models/__init__.py models/user.py
touch schemas/user_schemas.py
touch services/user_service.py
touch routes/user_routes.py routes/health_routes.py
```

### 2. Requirements (requirements.txt)

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-RESTX==1.2.0
PyMySQL==1.1.0
python-dotenv==1.0.0
```

### 3. Environment Variables (.env) - Optional

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/mydatabase
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
```

## Installation and Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. MySQL Database Setup

```sql
CREATE DATABASE mydatabase;
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Update Configuration

Edit `config.py` and update the database URL:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://your_username:your_password@localhost/your_database'
```

### 4. Run the Application

```bash
python app.py
```

## Architecture Overview

### **Separation of Concerns**

1. **app.py** - Application factory and main entry point
2. **config.py** - Configuration management
3. **models/** - Database models and ORM operations
4. **schemas/** - API documentation and validation schemas
5. **services/** - Business logic and data processing
6. **routes/** - REST API endpoints and controllers

### **Layer Responsibilities**

- **Models Layer**: Database operations, ORM models
- **Service Layer**: Business logic, validation, data processing
- **Controller Layer**: HTTP request/response handling, API documentation
- **Schema Layer**: Request/response validation and API documentation

## Key Features

### **Database Layer (models/)**
- SQLAlchemy ORM models
- Database operations (CRUD)
- Model methods for common operations

### **Service Layer (services/)**
- Business logic separation
- Data validation
- Error handling
- Transaction management

### **API Layer (routes/)**
- REST endpoints
- Request validation
- Response formatting
- Swagger documentation

### **Configuration Management**
- Environment-based configuration
- Database connection pooling
- Development/Production configs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | Get all users |
| POST | `/users/` | Create a new user |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |
| GET | `/health` | Health check |

## Usage Examples

### Create User
```bash
curl -X POST http://localhost:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
```

### Get All Users
```bash
curl http://localhost:5000/users/
```

### Update User
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith", "age": 31}'
```

## Benefits of This Architecture

### **Maintainability**
- Clear separation of concerns
- Easy to locate and modify specific functionality
- Reduced code coupling

### **Scalability**
- Easy to add new models, services, or routes
- Service layer can be reused across different controllers
- Database operations are centralized

### **Testing**
- Each layer can be tested independently
- Mock services for controller testing
- Unit test business logic in isolation

### **Code Reusability**
- Service methods can be reused
- Models encapsulate database operations
- Schemas can be shared across endpoints

## Development Best Practices

1. **Error Handling**: Comprehensive error handling at each layer
2. **Validation**: Input validation at multiple levels
3. **Documentation**: Automatic Swagger documentation
4. **Configuration**: Environment-based configuration
5. **Database**: Connection pooling and transaction management

## Extending the API

### Adding a New Model

1. Create model in `models/new_model.py`
2. Create service in `services/new_service.py`
3. Create schemas in `schemas/new_schemas.py`
4. Create routes in `routes/new_routes.py`
5. Register namespace in `app.py`

### Example: Adding a Posts model

```python
# models/post.py
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
```

This modular structure makes it easy to maintain and extend your Flask API while keeping concerns properly separated.