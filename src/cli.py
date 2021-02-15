import click
import time
import os
import HtmlTestRunner

from src.environment.user_activities.user import User
from src.extensions import db


def register(app):
    @app.cli.command()
    @click.option(
        "--coverage/--no-coverage", default=False, help="Run tests under code coverage."
    )
    def test(coverage):

        if coverage:

            import coverage

            COV = coverage.coverage(branch=True, include="src/*")
            COV.start()

        import unittest

        tests = unittest.TestLoader().discover("src/tests")
        unittest.TextTestRunner(verbosity=2).run(tests)

        if coverage:
            COV.stop()
            COV.save()
            print("Coverage Summary:")
            COV.report()
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, "../tmp/coverage")
            COV.html_report(directory=covdir)
            COV.xml_report()
            print("HTML version: file://{}/index.html".format(covdir))
            COV.erase()

    @app.cli.command("create_user")
    def create_user():

        db.create_all()

        user = User("tuncutku10@gmail.com")
        user.set_password("1234")
        user.save_to_db()