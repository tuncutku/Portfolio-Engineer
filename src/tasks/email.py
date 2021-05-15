"""Email tasks."""
# pylint: disable=unused-argument, protected-access

from flask import current_app
from flask_mail import Message

from src.extensions import mail


def send_email(subject, recipients, html):
    """Send email with Flask-Mail."""

    app = current_app._get_current_object()
    msg = Message(subject, recipients, html)
    with app.app_context():
        mail.send(msg)
