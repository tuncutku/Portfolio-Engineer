from flask import Blueprint

from src.environment.portfolio import Portfolio


report_blueprint = Blueprint("report", __name__, url_prefix="/report")


@report_blueprint.route("/overview/<int:portfolio_id>", methods=["GET"])
def portfolio_overview(portfolio_id):

    Portfolio.find_by_id(portfolio_id)

    return "Hey"