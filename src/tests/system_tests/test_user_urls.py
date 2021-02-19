from flask_login import current_user

from src.tests.utils.base import BaseTest

from src.extensions import db
from src.environment.user import User

from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from flask_login import login_user

email = "tuncutku@gmail.com"
password = "1234"


class TestUserURLs(BaseTest):
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(User.find_by_email("test@gmail.com"))

        response = self.client.post(
            "/users/register",
            data=dict(email="test@gmail.com", password="1234", confirm="1234"),
            follow_redirects=True,
        )

        self.assertIsNotNone(User.find_by_email("test@gmail.com"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/users/register",
            data=dict(email="test_2@gmail.com", password="1234", confirm="12345"),
            follow_redirects=True,
        )

        self.assertTrue(
            "Field must be equal to password." in response.get_data(as_text=True)
        )

        self.assertIsNone(User.find_by_email("test_2@gmail.com"))

        response = self.client.post(
            "/users/register",
            data=dict(email="test@gmail.com", password="1234", confirm="1234"),
            follow_redirects=True,
        )

        self.assertTrue(
            "User with that email address already exists."
            in response.get_data(as_text=True)
        )

    def test_login_user(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(User.find_by_email("test@gmail.com"))
        user = User(email="test@gmail.com")
        user.set_password("1234")
        user.save_to_db()

        # Test wrong password
        response = self.client.post(
            "/users/login",
            data=dict(email="test@gmail.com", password="12345"),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid email or password" in response.get_data(as_text=True))

        # Test wrong email
        response = self.client.post(
            "/users/login",
            data=dict(email="test_3@gmail.com", password="12345"),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid email or password" in response.get_data(as_text=True))

        # Test correct email and password
        response = self.client.post(
            "/users/login",
            data=dict(email="test@gmail.com", password="1234"),
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("My Portfolios:" in response.get_data(as_text=True))

        self.assertTemplateUsed("portfolio/list_portfolios.html")
