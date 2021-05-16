"""Test peridic tasks"""
# pylint: disable=unused-argument

import pytest
from flask_mail import Mail

from src.environment import User
from src.tasks.messenger import daily_report_task, price_alert_task

task_list = [daily_report_task, price_alert_task]


@pytest.mark.parametrize(
    "task",
    task_list,
    ids=[task.name for task in task_list],
)
def test_tasks(client, _db, test_user, task):
    """Test daily alert periodic celery task."""

    with Mail().record_messages() as outbox:
        task.apply()
        assert len(outbox) == 1
