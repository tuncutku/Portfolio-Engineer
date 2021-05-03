import click
import time
import os
import pytest
import pytest_cov
import subprocess
from pylint import epylint

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

    @app.cli.command("check_style")
    def check_style():

        epylint.py_run("src")

    @app.cli.command("create_user")
    def create_user():

        db.create_all()

        user = User(email="tuncutku10@gmail.com")
        user.save_to_db()
        user.set_password("1234")
        user.confirm_user()

    @app.cli.command("clear_database")
    def clear_database():

        db.drop_all()
