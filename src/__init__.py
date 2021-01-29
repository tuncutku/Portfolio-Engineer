import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension

# from flask_celery import Celery
# from flask_caching import Cache
# from flask_mail import Mail
# from flask_login import LoginManager


# logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
# logging.getLogger().setLevel(logging.DEBUG)
# log = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()

# celery = Celery()
# cache = Cache()
# mail = Mail()

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'


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

    db.init_app(app)
    migrate.init_app(app, db)
    debug_toolbar.init_app(app)

    from src.views import (
        user_blueprint,
        account_blueprint,
        questrade_blueprint,
        position_blueprint,
        order_blueprint,
        home_blueprint,
    )

    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(account_blueprint, url_prefix="/account")
    app.register_blueprint(questrade_blueprint, url_prefix="/questrade")
    app.register_blueprint(position_blueprint, url_prefix="/position")
    app.register_blueprint(order_blueprint, url_prefix="/order")
    # app.register_blueprint(home_blueprint, url_prefix="/home")

    @app.route("/")
    def home():
        return render_template("home.html")

    return app
