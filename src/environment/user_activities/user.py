from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from src.extensions import db, bcrypt
from src.environment.user_activities.utils.encryption import (
    encrypt_token,
    decrypt_token,
)


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password = db.Column(db.String(255))

    portfolios_rs = db.relationship(
        "Portfolio", backref="user", cascade="all, delete-orphan"
    )

    def __init__(self, email: str):
        self.email = email

    def __repr__(self):
        return "<User {}>".format(self.email)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
