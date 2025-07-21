"""
Infra configurations
"""
import os


class Config:
    """Base configuration class"""
    DATABASE_URL = os.getenv('DATABASE_URL',
                             'mysql+pymysql://'
                             'appuser:apppassword@localhost:3306/'
                             'testdb?charset=utf8mb4&ssl_disabled=true')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 9100


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
