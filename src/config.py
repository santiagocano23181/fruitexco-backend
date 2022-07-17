from decouple import config

class Config:
    SECRET_KEY=config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{config("PGSQL_USER")}:{config("PGSQL_PASSWORD")}@{config("PGSQOL_HOST")}/{config("PGSQL_DATABASE")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
