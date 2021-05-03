# pylint: disable=no-member, invalid-name


from datetime import datetime
from typing import TypeVar, List

from flask import render_template

from src.tasks.email import send_email
from src.environment.utils.base import BaseModel


class Alert(BaseModel):
    """Base class for alerts."""

    __abstract__ = True

    @property
    def recipients(self) -> List[str]:
        """Email recipients."""
        raise NotImplementedError

    @property
    def subject(self) -> str:
        """Subject of the email."""
        raise NotImplementedError

    @property
    def email_template(self):
        """Email template to be used in the email."""
        raise NotImplementedError

    def condition(self) -> bool:
        """Condition to be checked before sending an email."""
        raise NotImplementedError

    def generate_email_content(self) -> dict:
        """Generate contents of the email."""
        raise NotImplementedError

    def send_async_email(self) -> None:
        """Send asynchronous email."""
        contents = self.generate_email_content()
        send_email.apply_async(
            subject=self.subject,
            recipients=self.recipients,
            html=render_template(self.email_template, **contents),
        )