import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
db_file = tempfile.NamedTemporaryFile()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # POSTS_PER_PAGE = 10

    # Celery config
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"

    # Mail config
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get("MAIL_SERVER_EMAIL")
    MAIL_PASSWORD = os.environ.get("MAIL_SERVER_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_SERVER_EMAIL")

    # Cash config
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST", "")
    CACHE_REDIS_PORT = "6379"
    CACHE_REDIS_PASSWORD = ""
    CACHE_REDIS_DB = "0"


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI", "")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "")
    RESULT_BACKEND = os.environ.get("CELERY_BROKER_URL", "")

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

    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USERNAME = "username"
    MAIL_PASSWORD = "password"
