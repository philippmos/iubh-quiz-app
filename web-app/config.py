from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, "env"))


class Config:

    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")



class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class StageConfig(Config):
    FLASK_ENV = 'staging'
    DEBUG = False
    TESTING = True


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
