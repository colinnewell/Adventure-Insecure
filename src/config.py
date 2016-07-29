import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'j1etLfY9D6ioCeJsUyXfNLguvB04O4bj'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/sessions'
    UPLOAD_FOLDER = '/tmp/upload'



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = DATABASE_URI = os.environ.get('CONNECTION_STRING')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'j1etLfY9D6ioCeJsUyXfNLguvB04O4bj'
    SESSION_FILE_DIR = os.environ.get('SESSION_DIR')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_DIR')
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
