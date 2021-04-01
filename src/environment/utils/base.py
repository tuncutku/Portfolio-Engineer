from abc import ABC, abstractmethod
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

    @property
    def subject(self):
        raise NotImplementedError

    @property
    def email_template(self):
        raise NotImplementedError

    def condition(self):
        raise NotImplementedError

    def send_email(self):
        raise NotImplementedError

    def activate(self) -> None:
        self.is_active = True
        db.session.commit()

    def deactivate(self) -> None:
        self.is_active = False
        db.session.commit()


class Security(BaseModel):
    __abstract__ = True

    symbol = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(3), nullable=False)
    currency = db.Column(db.String(3), nullable=False)

    @classmethod
    def find_by_symbol(cls, symbol: str):
        return cls.query.filter_by(symbol=symbol).first()

    def last_price(self):
        raise NotImplementedError

    def historical_price(self):
        raise NotImplementedError

    def periodic_prices(self):
        raise NotImplementedError
