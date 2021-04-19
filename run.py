import os
from dotenv import load_dotenv

from src import create_app
from src.cli import register_cli


load_dotenv()
app = create_app(os.getenv("FLASK_CONFIG"))
register_cli(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
