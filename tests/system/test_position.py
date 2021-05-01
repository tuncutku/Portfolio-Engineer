from src.environment.position import Position
from src.environment.order import Order

from tests.sample_data import *
from tests.system.common import templete_used


def test_position_details(client, _db, test_user, login, captured_templates):

    response = client.get("position/1/details")
    assert response.status_code == 200
    template_list = ["position/position_details.html"]
    templete_used(template_list, captured_templates)


def test_close_position(client, _db, test_user, login, captured_templates):

    pos = Position.find_by_id(1)
    assert pos.is_open is True
    response = client.get("position/1/close", follow_redirects=True)
    assert response.status_code == 200
    assert pos.is_open is False

    template_list = ["portfolio/list_portfolios.html"]
    templete_used(template_list, captured_templates)
