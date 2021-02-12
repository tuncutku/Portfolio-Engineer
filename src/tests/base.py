from flask_testing import TestCase

from src.extensions import db
from src import create_app


class BaseTest(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()