from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from src import db_1, bcrypt
from src.environment.user_activities.utils.encryption import (
    encrypt_token,
    decrypt_token,
)


class User(db_1.Model, UserMixin, SerializerMixin):
    __tablename__ = "users"
    id = db_1.Column(db_1.Integer(), primary_key=True)
    email = db_1.Column(db_1.String(255), nullable=False, index=True, unique=True)
    password = db_1.Column(db_1.String(255))

    def __init__(self, email: str):
        self.email = email

    def __repr__(self):
        return "<User {}>".format(self.email)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
