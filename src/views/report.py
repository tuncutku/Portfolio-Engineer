from flask import Blueprint, session, redirect
from flask_login import current_user, login_required

from src.environment.portfolio import Portfolio


report_blueprint = Blueprint("report", __name__, url_prefix="/report")


@report_blueprint.route("/report/<int:portfolio_id>", methods=["GET"])
@login_required
def view_report(portfolio_id):
    session["user_id"] = current_user.id
    session["portfolio_id"] = portfolio_id
    return redirect("/report/")