"""Email tasks."""
# pylint: disable=unused-argument, protected-access

from flask_mail import Message

from src.extensions import mail


def send_email(subject, recipients, html):
    """Send email with Flask-Mail."""

    msg = Message(subject, recipients, html=html)
    mail.send(msg)
