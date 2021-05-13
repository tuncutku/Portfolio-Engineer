"""Email tasks."""
# pylint: disable=unused-argument, protected-access

from flask import current_app
from flask_mail import Message

from src.extensions import mail, celery_logger
from src.extensions import celery


@celery.task(bind=True, ignore_result=True, default_retry_delay=300, max_retries=5)
def send_email(self, subject, recipients, html):
    """Background task to send an async email with Flask-Mail."""

    app = current_app._get_current_object()
    msg = Message(subject, recipients, html)
    celery_logger.info("Sending email.")
    with app.app_context():
        mail.send(msg)
