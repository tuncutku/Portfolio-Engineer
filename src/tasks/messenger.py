"""Daily tasks."""
# pylint: disable=unused-argument

from src.extensions import celery_logger, celery
from src.environment import User, Alert
from src.tasks.email import send_email


def send_alert_email(alert: Alert) -> None:
    """Send email with the given alert."""
    email = alert.generate_email()
    send_email(email.subject, email.recipients, email.html)


@celery.task(bind=True, name="daily_report")
def daily_report_task(self):
    """Background task to send an email with Flask-Mail."""
    for user in User.find_all():
        for portfolio in user.portfolios:
            alert = portfolio.daily_report
            open_positions = portfolio.get_open_positions()
            if alert.active and alert.condition and open_positions:
                celery_logger.info("Condition satisfied, preparing email.")
                send_alert_email(alert)


@celery.task(bind=True, name="price_alert")
def price_alert_task(self):
    """Background task to send an email with Flask-Mail."""
    for user in User.find_all():
        for alert in user.price_alerts:
            if alert.active and alert.condition():
                celery_logger.info("Condition satisfied, preparing email.")
                send_alert_email(alert)
                celery_logger.info("Price alert was triggered, deactivating the alert.")
                alert.deactivate()
