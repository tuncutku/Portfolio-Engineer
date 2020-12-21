from flask import Blueprint, request, session, url_for, render_template, redirect
import requests

from src.environment.user_activities import User #Portfolio
from src.environment.user_activities.utils import UserError, requires_login, requires_questrade_access
from src.questrade import Questrade
from src.views.reports.utils.report import valid_position

portfolio_blueprint = Blueprint("portfolio", __name__)


@portfolio_blueprint.route("/overview", methods=["GET"])
@requires_login
def overview():
    if not valid_position():
        return {"hello": "hey"}

    return "Hello world!"

def edit_portfolio():
    pass