from flask import Blueprint, render_template


home_blueprint = Blueprint("home", __name__)

# TODO: Enable user to sort the positions by -> Amount, price, date etc.
@home_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")
