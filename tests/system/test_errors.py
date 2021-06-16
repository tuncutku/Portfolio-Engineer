"""Test error handlings"""

from tests.system.common import templete_used


def test_unauthorized_request(client, captured_templates):
    """System test for add order endpoint."""

    response = client.get("/portfolio/list", follow_redirects=True)
    assert response.status_code == 200

    template_list = ["user/login.html"]
    templete_used(template_list, captured_templates)
