"""Run flask app"""

import os
from dotenv import load_dotenv

from src import create_app


load_dotenv()
port = int(os.environ.get("PORT", 5001))
app = create_app(os.getenv("FLASK_CONFIG"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
