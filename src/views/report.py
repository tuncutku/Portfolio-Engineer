"""Dashboard endpoints"""

from flask import Blueprint, url_for, redirect
from flask_login import current_user, login_required


report_blueprint = Blueprint("report", __name__, url_prefix="/report")


@report_blueprint.route("/report/", methods=["GET"])
@login_required
def view_report():
    """Direct user to dashboard."""
    empty_port_check = [bool(port.positions) for port in current_user.portfolios]

    if any(empty_port_check):
        return redirect("/report/")
    return redirect(url_for("portfolio.list_portfolios"))
