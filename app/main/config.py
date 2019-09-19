import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ajocard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True
    SWAGGER_UI_JSONEDITOR = True
    RESTPLUS_VALIDATE = True
    SWAGGER_UI_DOC_EXPANSION = 'list'



class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
AUTH_LOGIN = 1
API_TOKEN_KEY='trustedcoder'
RESET_PASSWORD = 2
key_forgot_password = "4567890-jhgvcgbuhvbnjhtyughkn "
ACTIVE = 1
ACTIVE_USER = 1