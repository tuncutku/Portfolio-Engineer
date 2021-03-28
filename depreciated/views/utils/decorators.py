import functools
from typing import Callable
from flask import (
    session,
    flash,
    redirect,
    url_for,
    request,
    current_app,
    render_template,
)

from src.questrade import Questrade, Questrade_Account, Questrade_Market_Data
from src.questrade.utils import (
    TokenNotFoundError,
    InternalServerError,
    InvalidTokenError,
)


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("email"):
            flash("You need to be signed in for this page.", "danger")
            return redirect(url_for("users.login"))

        # ONLY FOR DEVELOPMENT!!!!!
        # import os
        # email = os.environ["ADMIN_EMAIL"]
        # session["email"] = email

        return f(*args, **kwargs)

    return decorated_function


def requires_questrade_access(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        q = Questrade_Account()
        try:
            q.access_status()
        except (TokenNotFoundError, InvalidTokenError) as e:
            return render_template(
                "account/questrade_token.html", error_message=e.message
            )
        except InternalServerError as e:
            return redirect(url_for("portfolio.list_portfolios"))
        return f(q=q, *args, **kwargs)

    return decorated_function


def market_data_connection(f: Callable) -> Callable:
    @functools.wraps(f)
    @requires_questrade_access
    def decorated_function(q: Questrade, *args, **kwargs):
        md = Questrade_Market_Data()
        return f(md=md, *args, **kwargs)

    return decorated_function
