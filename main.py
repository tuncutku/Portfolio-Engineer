import os
from src import create_app
from src.cli import register_cli

app = create_app("config.DevConfig")
register_cli(app)


if __name__ == "__main__":
    app.run()