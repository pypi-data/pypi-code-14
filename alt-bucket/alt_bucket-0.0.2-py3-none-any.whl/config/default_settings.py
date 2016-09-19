class DefaultConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'


class DevConfig(DefaultConfig):
    DEBUG = True
