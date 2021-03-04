import logging
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_session import Session


import ssl

ssl._create_default_https_context = ssl._create_unverified_context


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


db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap()
sess = Session()

# Configure login manager
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

# Necessary for the Dash to functioni
csrf._exempt_views.add("dash.dash.dispatch")


@login_manager.user_loader
def load_user(userid):
    from src.environment.user import User

    return User.find_by_id(userid)


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for("users.login"))


# celery = Celery()
# cache = Cache()
# mail = Mail()