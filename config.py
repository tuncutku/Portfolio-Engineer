"""App ocnfiguration"""
# pylint: disable=too-few-public-methods, consider-using-with

import os
import tempfile
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
db_file = tempfile.NamedTemporaryFile()

load_dotenv()


class ConfigBase:
    """Base class for configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECRET_KEY")

    # Celery config
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail config
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get("MAIL_SERVER_EMAIL")
    MAIL_PASSWORD = os.environ.get("MAIL_SERVER_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_SERVER_EMAIL")

    WTF_CSRF_TIME_LIMIT = None


class HerokuConfig(ConfigBase):
    """Configuration for Heroku deployment."""

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    RESULT_BACKEND = os.environ.get("CELERY_BROKER_URL")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class DockerConfig(ConfigBase):
    """Configuration for local docker setup."""

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:password@postgres:5432/db"
    DEBUG = True


class DevConfig(ConfigBase):
    """Configuration for development."""

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG = True


class TestConfig(ConfigBase):
    """Configuration for testing."""

    TESTING = True
    DEBUG = True
    DEBUG_TB_ENABLED = False
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, db_file.name)


config = {
    "heroku": HerokuConfig,
    "development": DevConfig,
    "testing": TestConfig,
    "docker": DockerConfig,
}
