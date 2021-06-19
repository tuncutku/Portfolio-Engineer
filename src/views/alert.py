"""Alert endpoints"""

from typing import Union
from flask import Blueprint, url_for, render_template, redirect, flash
from flask_login import login_required, current_user

from src.forms import AddAlertForm, AddMarketWatchInstrument
from src.environment import User, MarketAlert, WatchListInstrument
from src.market import Instrument, Symbol, get_instrument
from src.market.ref_data import up, down, up_equal, down_equal
from src.market.signal import (
    Signal,
    DailyPortfolioReturnSignal,
    DailyReturnSignal,
    PriceSignal,
    LimitReturnSignal,
    PortfolioValueSignal,
)


alert_blueprint = Blueprint("alert", __name__, url_prefix="/alert")


@alert_blueprint.route("/list", methods=["GET"])
@login_required
def list_alerts():
    """List alerts."""

    user: User = current_user
    return render_template("alert/list_alerts.html", alerts=user.market_alerts)


@alert_blueprint.route("/add_alert", methods=["GET", "POST"])
@login_required
def add_alert():
    """Add new alert."""

    user: User = current_user
    alert_form = AddAlertForm()

    if alert_form.validate_on_submit():
        signal = get_signal(
            alert_form.signal.data,
            alert_form.underlying.data,
            alert_form.operator.data,
            alert_form.target.data,
            alert_form.start_date.data,
        )

        if signal not in [alert.signal for alert in user.market_alerts]:
            user.add_market_alert(MarketAlert(signal))
            return redirect(url_for("alert.list_alerts"))
        flash("Market alert already exists, please activate it.", "danger")

    return render_template("alert/add_alert.html", form=alert_form)


@alert_blueprint.route("/deactivate_alert/<int:alert_id>", methods=["GET"])
@login_required
def deactivate_alert(alert_id):
    """Deactivate alert."""

    alert = MarketAlert.find_by_id(alert_id)
    alert.deactivate()
    return redirect(url_for("alert.list_alerts"))


@alert_blueprint.route("/activate_alert/<int:alert_id>", methods=["GET"])
@login_required
def activate_alert(alert_id):
    """Activate alert."""

    alert = MarketAlert.find_by_id(alert_id)
    alert.activate()
    return redirect(url_for("alert.list_alerts"))


@alert_blueprint.route("/delete_alert/<int:alert_id>", methods=["GET"])
@login_required
def delete_alert(alert_id):
    """Delete alert."""

    alert = MarketAlert.find_by_id(alert_id)
    alert.delete_from_db()
    return redirect(url_for("alert.list_alerts"))


@alert_blueprint.route("/watchlist", methods=["GET", "POST"])
@login_required
def list_watchlist():
    """List alert."""

    user: User = current_user
    form = AddMarketWatchInstrument()

    if form.validate_on_submit():
        watchlist_inst = WatchListInstrument(get_instrument(Symbol(form.symbol.data)))
        user.add_watchlist_instrument(watchlist_inst)
        return redirect(url_for("alert.list_watchlist"))

    return render_template(
        "alert/watchlist.html", instruments=user.watch_list, form=form
    )


@alert_blueprint.route("/delete_watchlist/<int:inst_id>", methods=["GET"])
@login_required
def delete_watchlist_instrument(inst_id):
    """Delete watchlist instrument."""

    watchlist_inst = WatchListInstrument.find_by_id(inst_id)
    watchlist_inst.delete_from_db()
    return redirect(url_for("alert.list_watchlist"))


def get_signal(
    signal: str, underlying: Union[Instrument, str], operator, target, start_date
) -> Signal:
    """Get underlying portfolio or instrument."""

    operator_dict = {
        "Up": up,
        "Up or Equal": up_equal,
        "Down": down,
        "Down or Equal": down_equal,
    }
    operator = operator_dict[operator]
    signal_dict = {
        "Price Signal": lambda: PriceSignal(
            get_instrument(Symbol(underlying)), operator, target
        ),
        "Daily Return Signal": lambda: DailyReturnSignal(
            get_instrument(Symbol(underlying)), operator, target
        ),
        "Limit Return Signal": lambda: LimitReturnSignal(
            get_instrument(Symbol(underlying)), operator, target, start_date
        ),
        "Portfolio Value Signal": lambda: PortfolioValueSignal(
            underlying, operator, target
        ),
        "Daily Portfolio Return Signal": lambda: DailyPortfolioReturnSignal(
            underlying, operator, target
        ),
    }

    func = signal_dict[signal]
    return func()
