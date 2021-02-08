from flask import Flask, render_template

from src.extensions import (
    db,
    migrate,
    debug_toolbar,
    bcrypt,
    login_manager,
    csrf,
    bootstrap,
)
from src.views import (
    user_blueprint,
    portfolio_blueprint,
    order_blueprint,
    error_handler_blueprint,
)


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
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    # TODO: use the feature of bootstrap.
    bootstrap.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(portfolio_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(error_handler_blueprint)

    @app.route("/")
    def home():
        db.create_all()
        return render_template("home.html")

    return app
