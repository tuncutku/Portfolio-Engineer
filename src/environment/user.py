from datetime import datetime
from flask_login import UserMixin

from src.environment.utils.base import BaseModel
from src.extensions import db, bcrypt


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password = db.Column(db.String(255))
    confirmed = db.Column(db.Boolean(), default=False)

    portfolios = db.relationship(
        "Portfolio", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, email: str):
        self.email = email

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
