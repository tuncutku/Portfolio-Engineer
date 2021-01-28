from src.environment.user_activities.user import User


def test_create_user():
    """Unit test to check user attributes."""

    user_email = "test_user@gmail.com"
    user_password = "12345678"
    user = User(user_email, user_password)

    user_dict = {"email": "test_user@gmail.com", "password": "12345678"}

    for attribute, output in user_dict.items():
        assert getattr(user, attribute) == output
