import ssl
from flask import redirect, url_for

ssl._create_default_https_context = ssl._create_unverified_context

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# from flask_caching import Cache
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from celery import Celery

import logging
from celery.utils.log import get_task_logger

celery_logger = get_task_logger(__name__)

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger(__name__)


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
# cache = Cache()
mail = Mail()
jwt = JWTManager()
celery = Celery()

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
