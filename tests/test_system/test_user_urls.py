import pytest

from flask_mail import Mail
from src.environment.user import User
from src.views.user import generate_confirmation_token

from tests.test_system.common import templete_used
from tests.utils import create_user


email = "tuncutku@gmail.com"
password = "1234"


def test_home(client, _db, captured_templates):
    response = client.get("/")
    assert response.status_code == 200

    template_list = ["home.html"]
    templete_used(template_list, captured_templates)


def test_register_user(client, _db, captured_templates, request, mocker):

    mail = Mail()

    response = client.get("/users/register")

    assert response.status_code == 200
    assert User.find_by_email("test@gmail.com") is None

    with mail.record_messages() as outbox:

        response = client.post(
            "/users/register",
            data=dict(email="test@gmail.com", password="1234", confirm="1234"),
            follow_redirects=True,
        )

        assert len(outbox) == 1
        assert outbox[0].subject == "Account confirmation - Portfolio Engineer"

    assert User.find_by_email("test@gmail.com") is not None
    assert response.status_code == 200

    response = client.post(
        "/users/register",
        data=dict(email="test_2@gmail.com", password="1234", confirm="12345"),
        follow_redirects=True,
    )

    assert "Field must be equal to password." in response.get_data(as_text=True)
    assert User.find_by_email("test_2@gmail.com") is None

    response = client.post(
        "/users/register",
        data=dict(email="test@gmail.com", password="1234", confirm="1234"),
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


def test_login_user(client, _db, captured_templates):
    response = client.get("/users/login")
    assert response.status_code == 200

    assert User.find_by_email("test@gmail.com") is None
    create_user(email="test@gmail.com", password="1234")

    # Test wrong password
    response = client.post(
        "/users/login",
        data=dict(email="test@gmail.com", password="12345"),
        follow_redirects=True,
    )

    # Test wrong email
    emails = ["test@gmail.com", "test_3@gmail.com"]
    passwords = ["12345", "1234"]

    for email, password in zip(emails, passwords):
        response = client.post(
            "/users/login",
            data=dict(email="test_3@gmail.com", password="1234"),
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
        data=dict(email="test@gmail.com", password="1234"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "My Portfolios:" in response.get_data(as_text=True)

    template_list = [
        "user/login.html",
        "user/login.html",
        "user/login.html",
        "user/login.html",
        "portfolio/list_portfolios.html",
    ]
    templete_used(template_list, captured_templates)


def test_email_confirmation(client, _db, captured_templates, request):

    create_user(email="test@gmail.com", password="1234", confirmed=False)
    user = User.find_by_id(1)
    assert user.confirmed is False

    token = generate_confirmation_token(user.email)
    response = client.get(f"/users/confirm/{token}", follow_redirects=True)

    assert user.confirmed is True

    template_list = ["user/login.html"]
    templete_used(template_list, captured_templates)