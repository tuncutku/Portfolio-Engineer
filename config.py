import os
import tempfile


basedir = os.path.abspath(os.path.dirname(__file__))
db_file = tempfile.NamedTemporaryFile()


class Config(object):
    SECRET_KEY = "736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b"
    # POSTS_PER_PAGE = 10

    CELERY_BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"

    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USER = "somemail@gmail.com"
    # MAIL_PASSWORD = "password"
    # MAIL_DEFAULT_SENDER = "from@flask.com"


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "")
    result_backend = os.environ.get("CELERY_BROKER_URL", "")

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST", "")
    CACHE_REDIS_PORT = "6379"
    CACHE_REDIS_PASSWORD = ""
    CACHE_REDIS_DB = "0"

    WTF_CSRF_TIME_LIMIT = None


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    CACHE_TYPE = "simple"

    WTF_CSRF_TIME_LIMIT = None


class TestConfig(Config):

    DEBUG = True
    DEBUG_TB_ENABLED = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, db_file.name)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    # CACHE_TYPE = "null"
    # MAIL_SERVER = "localhost"
    # MAIL_PORT = 25
    # MAIL_USERNAME = "username"
    # MAIL_PASSWORD = "password"
