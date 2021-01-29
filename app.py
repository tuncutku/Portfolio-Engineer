import os
from flask import Flask, render_template
import inspect

from scripts.db import create_tables, drop_tables
from src.views import (
    user_blueprint,
    account_blueprint,
    questrade_blueprint,
    position_blueprint,
    order_blueprint,
)


# TODO use plotly dash for dynamic graphics
# TODO use flask_profiler for monitoring endpoints
# TODO use flask-swagger for profiling
# youtube tutorial: https://www.youtube.com/channel/UCqBFsuAz41sqWcFjZkqmJqQ/playlists (Charming Data)
app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

app.secret_key = os.urandom(64)
# app.config.update(ADMIN=os.environ.get("ADMIN"))

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(account_blueprint, url_prefix="/account")
app.register_blueprint(questrade_blueprint, url_prefix="/questrade")
app.register_blueprint(position_blueprint, url_prefix="/position")
app.register_blueprint(order_blueprint, url_prefix="/order")


@app.before_first_request
def initiate_tables():
    # drop_tables()
    # create_tables()
    return


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=5000)
