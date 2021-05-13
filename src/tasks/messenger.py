"""Daily tasks."""
# pylint: disable=unused-argument

from src.extensions import celery_logger, celery
from src.environment import User
from src.tasks.email import send_email


@celery.task(bind=True, name="daily_report")
def daily_report_task(self):
    """Background task to send an email with Flask-Mail."""
    for user in User.find_all():
        for portfolio in user.portfolios:
            alert = portfolio.daily_report
            open_positions = [
                position for position in portfolio.positions if position.is_open
            ]
            if alert.active and alert.condition and open_positions:
                celery_logger.info("Condition satisfied, preparing email.")
                email = alert.generate_email()
                send_email(email.subject, email.recipients, email.html)
