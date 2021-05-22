"""Test user object"""
# pylint: disable=unused-argument

from src.environment import User
from tests.test_data import environment as env


def test_user_object(client, _db, load_environment_data):
    """Test saved user object."""

    user = User.find_by_id(1)

    assert user.id == 1
    assert user.email == env.user_1_raw["email"]
    assert repr(user) == "<User tuncutku10@gmail.com.>"
    assert user.confirmed is True

    assert user == User.find_by_email(env.user_1_raw["email"])
    assert user.check_password(env.user_1_raw["password"])
