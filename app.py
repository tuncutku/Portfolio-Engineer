import os
from flask import Flask, render_template

from src.db import create_tables
from src.app.views.user import user_blueprint

app = Flask(__name__, template_folder='src/app/templates')

app.secret_key = os.urandom(64)
app.config.update(ADMIN=os.environ.get("ADMIN"))

app.register_blueprint(user_blueprint, url_prefix="/users")

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    # create_tables()
    app.run(debug=True, host="0.0.0.0", port=5000)
