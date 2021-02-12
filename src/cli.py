import click
import time
import os


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
            print("HTML version: file://{covdir}/index.html")
            COV.erase()
