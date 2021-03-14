from flask import Blueprint, url_for, redirect
from flask_login import current_user, login_required


from src.environment.portfolio import Portfolio


report_blueprint = Blueprint("report", __name__, url_prefix="/report")


@report_blueprint.route("/report/", methods=["GET"])
@login_required
def view_report():
    empty_port_check = [
        True if port.positions else False for port in current_user.portfolios
    ]

    if any(empty_port_check):
        return redirect("/report/")
    else:
        return redirect(url_for("portfolio.list_portfolios"))