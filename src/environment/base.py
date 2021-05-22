"""Base classes for environment objects"""
# pylint: disable=no-member, invalid-name

from datetime import datetime
from collections import namedtuple
from typing import TypeVar, List
from flask import render_template

from src.extensions import db

T = TypeVar("T", bound="BaseModel")
Email = namedtuple("Email", ["subject", "recipients", "html"])


class BaseModel(db.Model):
    """Base class for user activities."""

    __abstract__ = True

    id: int = db.Column(db.Integer(), primary_key=True)
    creation_date: datetime = db.Column(db.DateTime(), default=datetime.now)

    @classmethod
    def find_by_id(cls: T, _id: int) -> T:
        """Find object by id."""
        return cls.query.get(_id)

    @classmethod
    def find_all(cls: T) -> List[T]:
        """Find all objects."""
        return cls.query.all()

    def save_to_db(self) -> None:
        """Save object to db."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Delete object from db."""
        db.session.delete(self)
        db.session.commit()


class Alert(BaseModel):
    """Base class for alerts."""

    __abstract__ = True

    active = db.Column(db.Boolean(), default=False)

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

    def activate(self) -> None:
        """Activate alert."""
        self.active = True
        db.session.commit()

    def deactivate(self) -> None:
        """Deactivate alert."""
        self.active = False
        db.session.commit()

    def generate_email(self) -> Email:
        """Generate email object."""
        contents = self.generate_email_content()
        return Email(
            self.subject,
            self.recipients,
            render_template(self.email_template, **contents),
        )
