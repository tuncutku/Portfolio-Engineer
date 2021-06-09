"""Alert endpoints"""

from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required, current_user

from src.environment import User


alert_blueprint = Blueprint("alert", __name__, url_prefix="/alert")


@alert_blueprint.route("/list", methods=["GET"])
@login_required
def list_alerts():
    """List alerts."""

    user: User = current_user

    return render_template("alert/list_alerts.html", alerts=user.market_alerts)
