from flask import Blueprint, session, redirect
from flask_login import current_user, login_required

from src.environment.portfolio import Portfolio


report_blueprint = Blueprint("report", __name__, url_prefix="/report")


@report_blueprint.route("/report/", methods=["GET"])
@login_required
def view_report():
    return redirect("/report/")