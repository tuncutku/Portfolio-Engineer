from src.environment.user import User

from tests.test_system.common import templete_used


email = "tuncutku@gmail.com"
password = "1234"


def test_home(client, db, captured_templates):
    response = client.get("/")
    assert response.status_code == 200

    template_list = ["home.html"]
    templete_used(template_list, captured_templates)


def test_register_user(client, db, captured_templates):
    response = client.get("/users/register")

    assert response.status_code == 200
    assert User.find_by_email("test@gmail.com") == None

    response = client.post(
        "/users/register",
        data=dict(email="test@gmail.com", password="1234", confirm="1234"),
        follow_redirects=True,
    )

    assert User.find_by_email("test@gmail.com") != None
    assert response.status_code == 200

    response = client.post(
        "/users/register",
        data=dict(email="test_2@gmail.com", password="1234", confirm="12345"),
        follow_redirects=True,
    )

    assert "Field must be equal to password." in response.get_data(as_text=True)
    assert User.find_by_email("test_2@gmail.com") == None

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
        "user/login.html",
        "user/register.html",
        "user/register.html",
    ]
    templete_used(template_list, captured_templates)


def test_login_user(client, db, captured_templates):
    response = client.get("/users/login")
    assert response.status_code == 200

    assert User.find_by_email("test@gmail.com") == None
    user = User(email="test@gmail.com")
    user.set_password("1234")
    user.save_to_db()

    # Test wrong password
    response = client.post(
        "/users/login",
        data=dict(email="test@gmail.com", password="12345"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Invalid email or password" in response.get_data(as_text=True)

    # Test wrong email
    response = client.post(
        "/users/login",
        data=dict(email="test_3@gmail.com", password="12345"),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Invalid email or password" in response.get_data(as_text=True)

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
        "portfolio/list_portfolios.html",
    ]
    templete_used(template_list, captured_templates)
