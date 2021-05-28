"""Create app and celery"""
# pylint: disable=too-few-public-methods

from flask import Flask, render_template, has_app_context
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from celery import Celery
from celery.schedules import crontab

from config import config

from src.extensions import (
    db,
    migrate,
    bcrypt,
    login_manager,
    csrf,
    # cache,
    mail,
    jwt,
)
from src.views import (
    user_blueprint,
    portfolio_blueprint,
    position_blueprint,
    order_blueprint,
    error_handler_blueprint,
    report_blueprint,
    alert_blueprint,
    home_blueprint,
)

# from src.dashapp import register_dash_app


def create_app(object_name=None):
    """
    Flask application factory

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(config[object_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # cache.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(portfolio_blueprint)
    app.register_blueprint(position_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(error_handler_blueprint)
    app.register_blueprint(report_blueprint)
    app.register_blueprint(alert_blueprint)
    app.register_blueprint(home_blueprint)

    # register_dash_app(app)
    make_celery(app)

    return app


def make_celery(app):
    """Make celery app."""
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["RESULT_BACKEND"],
    )
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        "periodic_task-every-minute": {
            "task": "daily_report",
            "schedule": crontab(minute="*"),
        },
        "periodic_task_2-every-minute": {
            "task": "market_alert",
            "schedule": crontab(minute="*"),
        },
    }
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """Form context task object."""

        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
