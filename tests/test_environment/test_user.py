from tests.sample_data import user_1
from tests.utils import create_user

from src.environment.user import User


def test_user(client, _db):
    """Integration test for users."""

    # Create user
    assert User.find_by_email(email=user_1["email"]) is None
    user = User(email=user_1["email"])
    user.set_password(user_1["password"])
    user.save_to_db()
    assert User.find_by_email(email=user_1["email"]) is not None
    assert User.find_by_id(1) is not None

    # Test basic attributes
    assert user.id == 1
    assert user.email == "tuncutku10@gmail.com"
    assert user.confirmed is False
    assert repr(user) == "<User tuncutku10@gmail.com.>"

    # Test methods
    assert user.check_password(user_1["password"]) is True
    user.confirm_user()
    assert user.confirmed is True

    # Delete user
    user.delete_from_db()
    assert User.find_by_email(email=user_1["email"]) is None
