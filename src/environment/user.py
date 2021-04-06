from datetime import datetime
from flask_login import UserMixin
from typing import List

from src.environment.utils.base import BaseModel
from src.environment.portfolio import Portfolio
from src.extensions import db, bcrypt


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    email: str = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password: str = db.Column(db.String(255))
    confirmed: bool = db.Column(db.Boolean(), default=False)

    portfolios: List[Portfolio] = db.relationship(
        "Portfolio", backref="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}.>"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def confirm_user(self) -> None:
        self.confirmed = True
        db.session.commit()

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()
