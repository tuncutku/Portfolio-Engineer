import os
from flask import Flask, render_template
import inspect

from src.app.db import create_tables
from src.app.views import *

# TODO use plotly dash for dynamic graphics
# youtube tutorial: https://www.youtube.com/channel/UCqBFsuAz41sqWcFjZkqmJqQ/playlists (Charming Data)
app = Flask(__name__, template_folder="src/app/templates", static_folder="src/app/static")

app.secret_key = os.urandom(64)
app.config.update(ADMIN=os.environ.get("ADMIN"))

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(account_blueprint, url_prefix="/account")
app.register_blueprint(portfolio_blueprint, url_prefix="/portfolio")
app.register_blueprint(questrade_blueprint, url_prefix="/questrade")

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    create_tables()
    # create_guest_user()
    app.run(debug=True, host="0.0.0.0", port=5000)
