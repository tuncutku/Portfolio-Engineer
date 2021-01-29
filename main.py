import os
from src import create_app
from src.cli import register

app = create_app("config.DevConfig")
register(app)


if __name__ == "__main__":
    app.run()