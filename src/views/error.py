from flask import Blueprint, request, session, url_for, render_template, redirect
from flask_login import login_required, current_user

from src.questrade.utils import TokenError


error_handler_blueprint = Blueprint(
    "error_handler", __name__, url_prefix="/error_handler"
)


@error_handler_blueprint.app_errorhandler(TokenError)
def questrade_access_denied(err):

    a = 1
    return render_template("account/questrade_token.html", error_message=None)