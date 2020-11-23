import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app

from lib.questrade.questrade import Questrade
from lib.questrade.utils import TokenNotFoundError
from src.app.models.auth import Auth


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("email"):
            flash("You need to be signed in for this page.", "danger")
            return redirect(url_for("users.login_user"))
        return f(*args, **kwargs)
    return decorated_function


def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") != current_app.config.get("ADMIN", ""):
            flash("You need to be an administrator to access this page.", "danger")
            return redirect(url_for("users.login_user"))
        return f(*args, **kwargs)
    return decorated_function


def requires_questrade_access(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        q = Questrade()
        try:
            q.access_status()
        except TokenNotFoundError:
            return redirect(url_for("questrade.insert_refresh_token"))
        return f(*args, **kwargs)
    return decorated_function