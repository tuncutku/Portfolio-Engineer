from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar, List

from src.extensions import db

T = TypeVar("T", bound="BaseModel")


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    creation_date = db.Column(db.DateTime(), default=datetime.now)

    @classmethod
    def find_by_id(cls: T, _id: int) -> T:
        return cls.query.get(_id)

    @classmethod
    def find_all(cls: T) -> List[T]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class AlertBase(BaseModel):
    __abstract__ = True

    @property
    def recipients(self) -> List[str]:
        raise NotImplementedError

    @property
    def subject(self) -> str:
        raise NotImplementedError

    @property
    def email_template(self):
        raise NotImplementedError

    def condition(self) -> bool:
        raise NotImplementedError

    def generate_email_content(self) -> dict:
        raise NotImplementedError

    def send_async_email(self) -> None:
        contents = self.generate_email_content()
        send_email.apply_async(
            subject=self.subject,
            recipients=self.recipients,
            html=render_template(self.email_template, **contents),
        )
