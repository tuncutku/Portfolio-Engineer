from flask import Blueprint, request, session, url_for, render_template, redirect
import requests

from src.environment.user_activities import User #Portfolio
from src.environment.user_activities.utils import UserError, requires_login, requires_questrade_access
from src.services.questrade import Questrade

portfolio_blueprint = Blueprint("portfolio", __name__)


@portfolio_blueprint.route("/overview", methods=["GET"])
@requires_login
def portfolio_overview():
    if not valid_positions:
        return 

    return "Hello world!"

def edit_portfolio():
    pass