from abc import ABC, abstractmethod
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

from src.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    creation_date = db.Column(db.DateTime(), default=datetime.now)

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.get(_id)

    @classmethod
    def find_all(cls) -> list:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class AlertBaseModel(BaseModel):
    __abstract__ = True

    is_active = db.Column(db.Boolean(), default=False)
    quantity = db.Column(db.Integer(), nullable=False)

    @property
    def email_template(self):
        raise NotImplementedError

    def condition(self):
        raise NotImplementedError

    def is_satisfied(self):
        return True if self.condition else False

    def activate(self) -> None:
        self.is_active = True
        db.session.commit()

    def deactivate(self) -> None:
        self.is_active = False
        db.session.commit()


class OrderBaseModel(BaseModel):
    __abstract__ = True

    symbol = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    side = db.Column(db.String(255), nullable=False)
    avg_exec_price = db.Column(db.Float(), nullable=False)
    exec_time = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Float(), nullable=False)
