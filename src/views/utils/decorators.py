import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app, render_template

from src.questrade import Questrade
from src.questrade.utils import TokenNotFoundError, InternalServerError, InvalidTokenError

# ONLY FOR DEVELOPMENT!!!!!
import os

def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("email"):
            flash("You need to be signed in for this page.", "danger")
            return redirect(url_for("users.login_user"))

        # ONLY FOR DEVELOPMENT!!!!!
        # email = os.environ["ADMIN_EMAIL"]
        # session["email"] = email

        return f(*args, **kwargs)
    return decorated_function


def requires_questrade_access(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        q = Questrade()
        try:
            q.access_status()
        except (TokenNotFoundError, InvalidTokenError) as e:
            return render_template("account/questrade_token.html", error_message=e.message)
        # TODO add the error message to the webpage
        except InternalServerError as e:
            return redirect(url_for("account.list_portfolios"))
        return f(q=q, *args, **kwargs)
    return decorated_function

# TODO: check if all positions are valid.
def valid_positions(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function