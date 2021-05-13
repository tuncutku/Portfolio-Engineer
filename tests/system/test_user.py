"""Test user endpoints"""
# pylint: disable=unused-argument

from flask_mail import Mail
from src.environment.user import User
from src.views.user import generate_confirmation_token

from tests.system.common import templete_used
from tests.test_data.sample_data import user_1


def test_home(client, _db, captured_templates):
    """System test for home endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    template_list = ["home.html"]
    templete_used(template_list, captured_templates)


def test_register_user(client, _db, captured_templates):
    """System test for user register endpoint."""

    email = "test@gmail.com"
    password = "1234"

    response = client.get("/users/register")

    assert response.status_code == 200
    assert User.find_by_email(email) is None

    with Mail().record_messages() as outbox:

        response = client.post(
            "/users/register",
            data=dict(email=email, password=password, confirm=password),
            follow_redirects=True,
        )

        assert len(outbox) == 1
        assert outbox[0].subject == "Account confirmation - Portfolio Engineer"

    assert response.status_code == 200
    assert User.find_by_email(email)

    # Test wrong confirmation email.
    response = client.post(
        "/users/register",
        data=dict(email="test_2@gmail.com", password="1234", confirm="12345"),
        follow_redirects=True,
    )
    assert "Field must be equal to password." in response.get_data(as_text=True)
    assert not User.find_by_email("test_2@gmail.com")

    # Test registering existing user.
    response = client.post(
        "/users/register",
        data=dict(email=email, password=password, confirm=password),
        follow_redirects=True,
    )
    assert "User with that email address already exists." in response.get_data(
        as_text=True
    )

    template_list = [
        "user/register.html",
        "email/account_confirmation.html",
        "user/login.html",
        "user/register.html",
        "user/register.html",
    ]
    templete_used(template_list, captured_templates)


def test_login_user(client, _db, captured_templates, test_user):
    """System test for user login endpoint."""

    response = client.get("/users/login")
    assert response.status_code == 200

    # Test wrong email
    emails = ["test@gmail.com", "test_3@gmail.com"]
    passwords = ["12345", "1234"]

    for email, password in zip(emails, passwords):
        response = client.post(
            "/users/login",
            data=dict(email=email, password=password),
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert (
            "Invalid email, password or account has not been confirmed yet."
            in response.get_data(as_text=True)
        )

    # Test correct email and password
    response = client.post(
        "/users/login",
        data=dict(email=user_1["email"], password=user_1["password"]),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "My Portfolios:" in response.get_data(as_text=True)

    template_list = [
        "user/login.html",
        "user/login.html",
        "user/login.html",
        "portfolio/list_portfolios.html",
    ]
    templete_used(template_list, captured_templates)


def test_email_confirmation(client, _db, captured_templates):
    """System test for user email confirmation endpoint."""

    user = User(email="hello_world")
    user.save_to_db()

    assert not user.confirmed

    token = generate_confirmation_token(user.email)
    response = client.get(f"/users/confirm/{token}", follow_redirects=True)
    assert response.status_code == 200

    assert user.confirmed

    template_list = ["user/login.html"]
    templete_used(template_list, captured_templates)