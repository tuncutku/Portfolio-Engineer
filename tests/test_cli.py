"""Test CLI"""

import pytest


@pytest.fixture
def runner(client):
    """Generate test cli runner"""
    return client.application.test_cli_runner()


# def test_cli(runner):
#     """Test registered flask CLIs."""

#     result = runner.invoke(args=["init_db"])
