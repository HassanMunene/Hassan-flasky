import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'yoo my boy benzi')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'awanzihassan@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'xuhhwjkcsscxdmms'
    MAIL_SUBJECT = '[Flasky]'
    MAIL_SENDER = 'Flasky Admin <awanzihassan@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'sultanhamud081@gmail.com')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'mysql+mysqlconnector://hassan:munene14347@localhost/flasky'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'mysql+mysqlconnector://hassan:munene14347@localhost/testing'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URL = os.environ.get('PROD_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
