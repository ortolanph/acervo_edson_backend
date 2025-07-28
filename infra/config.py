"""
Infrastructure configurations.
"""
import dataclasses
import os


@dataclasses.dataclass
class Config:
    """Base configuration class"""
    DATABASE_URL = os.getenv('DATABASE_URL',
                             'mysql+pymysql://'
                             'appuser:apppassword@localhost:3306/'
                             'acervus_db?charset=utf8mb4&ssl_disabled=true')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 9100


@dataclasses.dataclass
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


@dataclasses.dataclass
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
