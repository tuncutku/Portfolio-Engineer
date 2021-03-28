from tests.sample_data import *
from tests.utils import create_user

from src.environment.user import User


def test_user(client, db):
    """Integration test for users."""

    # Create user
    assert User.find_by_email(email=user_1["email"]) == None
    user = create_user(**user_1)
    assert User.find_by_email(email=user_1["email"]) != None
    assert User.find_by_id(1) != None

    # Test basic attributes
    assert user.id == 1
    assert user.email == "tuncutku10@gmail.com"
    assert user.check_password(user_1["password"]) == True
    assert repr(user) == "<User tuncutku10@gmail.com.>"

    # Delete user
    user.delete_from_db()
    assert User.find_by_email(email=user_1["email"]) == None
