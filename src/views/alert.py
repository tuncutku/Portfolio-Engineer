"""Alert endpoints"""

from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required

from src.environment.portfolio import Portfolio


alert_blueprint = Blueprint("alert", __name__, url_prefix="/alert")


@alert_blueprint.route("/list/<int:portfolio_id>", methods=["GET"])
@login_required
def list_alerts(portfolio_id):
    """List alerts."""

    port = Portfolio.find_by_id(portfolio_id)
    daily_alert = port.daily_report

    return render_template(
        "alert/list_alerts.html",
        daily_alert_status=daily_alert.is_active,
        portfolio_id=portfolio_id,
    )


@alert_blueprint.route("/activate_daily_report/<int:portfolio_id>", methods=["GET"])
@login_required
def activate(portfolio_id):
    """Activate alert."""

    port = Portfolio.find_by_id(portfolio_id)
    port.daily_report.activate()

    return redirect(url_for("alert.list_alerts", portfolio_id=portfolio_id))


@alert_blueprint.route("/deactivate_daily_report/<int:portfolio_id>", methods=["GET"])
@login_required
def deactivate(portfolio_id):
    """Deactivate alert."""

    port = Portfolio.find_by_id(portfolio_id)
    port.daily_report.deactivate()

    return redirect(url_for("alert.list_alerts", portfolio_id=portfolio_id))
