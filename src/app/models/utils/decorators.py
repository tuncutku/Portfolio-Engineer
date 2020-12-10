import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app, render_template

from lib.questrade.questrade import Questrade
from lib.questrade.utils import TokenNotFoundError, InternalServerError, InvalidTokenError
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
        except (TokenNotFoundError, InvalidTokenError) as e:
            return render_template("portfolio/questrade/token.html", error_message=e.message)
        # TODO add the error message to the webpage
        except InternalServerError as e:
            return redirect(url_for("account.portfolio_list"))
        return f(*args, **kwargs)
    return decorated_function