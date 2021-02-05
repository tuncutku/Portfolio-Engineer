import logging
from dotenv import load_dotenv
from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap


import ssl

ssl._create_default_https_context = ssl._create_unverified_context

import yfinance as yf


load_dotenv()

# from flask_celery import Celery
# from flask_caching import Cache
# from flask_mail import Mail
# from flask_jwt_extended import JWTManager
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address


# logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
# logging.getLogger().setLevel(logging.DEBUG)
# log = logging.getLogger(__name__)


db_1 = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap()

# Configure login manager
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(userid):
    from src.environment.user_activities.user import User

    return User.query.get(userid)


# celery = Celery()
# cache = Cache()
# mail = Mail()


def create_app(object_name=None):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/
    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(object_name)

    db_1.init_app(app)
    migrate.init_app(app, db_1)
    debug_toolbar.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    # TODO: use the feature of bootstrap.
    bootstrap.init_app(app)

    from src.views import (
        user_blueprint,
        portfolio_blueprint,
        position_blueprint,
        order_blueprint,
        error_handler_blueprint,
    )

    app.register_blueprint(user_blueprint)
    app.register_blueprint(portfolio_blueprint)
    app.register_blueprint(position_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(error_handler_blueprint)

    @app.route("/")
    def home():
        db_1.create_all()
        return render_template("home.html")

    return app
