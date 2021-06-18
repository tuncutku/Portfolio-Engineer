"""Run flask app"""

import os
from dotenv import load_dotenv

from src import create_app


load_dotenv()
app = create_app(os.getenv("FLASK_CONFIG"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
