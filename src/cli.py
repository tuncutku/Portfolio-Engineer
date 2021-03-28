import click
import time
import os
import pytest
import pytest_cov
import subprocess

from src.environment.user import User
from src.extensions import db


def register_cli(app):
    @app.cli.command()
    @click.option(
        "--coverage/--no-coverage", default=False, help="Run tests under code coverage."
    )
    def test(coverage):

        if coverage:
            subprocess.call(
                [
                    "pytest",
                    "--cov=src",
                    "--cov-report",
                    "xml:cov.xml",
                    "--cov-config=.coveragerc",
                ]
            )
        else:
            subprocess.call(["pytest"])

    @app.cli.command("create_user")
    def create_user():

        db.create_all()

        user = User("tuncutku10@gmail.com")
        user.set_password("1234")
        user.save_to_db()

    @app.cli.command("clear_database")
    def clear_database():

        db.drop_all()
