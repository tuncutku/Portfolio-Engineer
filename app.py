import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='src/app/templates')

app.secret_key = os.urandom(64)
app.config.update(ADMIN=os.environ.get("ADMIN"))


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
