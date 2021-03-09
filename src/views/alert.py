from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required, current_user

from src.messenger.tasks import send_async_email


alert_blueprint = Blueprint("alert", __name__, url_prefix="/alert")


@alert_blueprint.route("/view_alerts/<int:portfolio_id>", methods=["GET"])
@login_required
def view_alerts(portfolio_id):

    content = {"email": current_user.email}

    send_async_email.apply_async(args=[content])

    a = 1


@alert_blueprint.route("/add_alert/<int:portfolio_id>", methods=["GET"])
@login_required
def add_alert(portfolio_id):

    content = {"email": current_user.email}

    send_async_email.apply_async(args=[content])

    a = 1