from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required, current_user
import pandas as pd


from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.forms.portfolio_forms import AddPortfolioForm, generate_edit_portfolio_form
from src.extensions import db

from src.views.reports import report_blueprint


@report_blueprint.route("/overview", methods=["GET"])
@login_required
def portfolio_overview():

    return "Hey"