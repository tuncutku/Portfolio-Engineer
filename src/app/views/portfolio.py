from flask import Blueprint, request, session, url_for, render_template, redirect
import requests

from src.app.models import User #Portfolio
from src.app.models.utils import UserError, requires_login, requires_questrade_access
from src.app.lib.questrade import Questrade

portfolio_blueprint = Blueprint("portfolio", __name__)


@portfolio_blueprint.route("/summary/overview", methods=["GET"])
@requires_login
def portfolio_overview():
    r = requests.get("http://127.0.0.1:5001")
    a =1
    #report = generate_portfolio_summary(p)
    return "Hello world!"

def edit_portfolio():
    pass