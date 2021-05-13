"""Test peridic tasks"""
# pylint: disable=unused-argument

from flask_mail import Mail

from src.tasks.messenger import daily_report_task


def test_daily_alert_task(client, _db, test_user, mock_symbol):
    """Test daily alert periodic celery task."""

    with Mail().record_messages() as outbox:
        daily_report_task.apply()

        assert len(outbox) == 1
