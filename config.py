from decouple import config
import os

class Config:
    SECRET_KEY=config("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{config("PGSQL_USER")}:{config("PGSQL_PASSWORD")}@{config("PGSQOL_HOST")}/{config("PGSQL_DATABASE")}'
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config("SECRET_KEY")
    TESTING = True
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
