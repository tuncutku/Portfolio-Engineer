"""User"""
# pylint: disable=no-member, cyclic-import

from typing import List

from flask_login import UserMixin

from src.environment.base import BaseModel
from src.environment.portfolio import Portfolio
from src.extensions import db, bcrypt
from src.market import Security, Currency


class User(BaseModel, UserMixin):
    """Form a user class."""

    __tablename__ = "users"

    email: str = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password: str = db.Column(db.LargeBinary())
    confirmed: bool = db.Column(db.Boolean(), default=False)

    portfolios: List[Portfolio] = db.relationship(
        "Portfolio", backref="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}.>"

    def set_password(self, password):
        """Set password for new user."""
        self.password = bcrypt.generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        """Validate given password by user."""
        return bcrypt.check_password_hash(self.password, password)

    def confirm_user(self) -> None:
        """Set user as confirmed."""
        self.confirmed = True
        db.session.commit()

    def add_portfolio(
        self,
        name: str,
        portfolio_type: str,
        reporting_currency: Currency,
        benchmark: Security,
    ) -> Portfolio:
        """Add new portfolio."""

        portfolio = Portfolio(
            name=name,
            portfolio_type=portfolio_type,
            reporting_currency=reporting_currency,
            benchmark=benchmark,
            user=self,
        )
        portfolio.save_to_db()
        return portfolio

    @classmethod
    def find_by_email(cls, email: str):
        """Find user by email."""
        return cls.query.filter_by(email=email).first()
