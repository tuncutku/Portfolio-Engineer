from flask import Flask, render_template
import json

from src.extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager,
    csrf,
    cache,
    mail,
    jwt,
    celery,
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
from src.dashapp import register_dash_app


def create_app(object_name=None):
    """
    Flask application factory

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(object_name)

    # Should be before "debug_toolbar"

    db.init_app(app)
    migrate.init_app(app, db)
    # debug_toolbar.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    celery.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(portfolio_blueprint)
    app.register_blueprint(position_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(error_handler_blueprint)
    app.register_blueprint(report_blueprint)
    app.register_blueprint(alert_blueprint)
    app.register_blueprint(home_blueprint)
    register_dash_app(app)

    return app
