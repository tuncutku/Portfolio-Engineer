"""User"""
# pylint: disable=no-member, cyclic-import

from typing import List

from flask_login import UserMixin

from src.environment.base import BaseModel
from src.environment.portfolio import Portfolio
from src.environment.alerts import MarketAlert
from src.extensions import db, bcrypt
from src.market import Security
from src.market.alerts import MarketSignal


class User(BaseModel, UserMixin):
    """Form a user class."""

    __tablename__ = "users"

    email: str = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password: str = db.Column(db.LargeBinary())
    confirmed: bool = db.Column(db.Boolean(), default=False)

    portfolios: List[Portfolio] = db.relationship(
        "Portfolio", back_populates="user", cascade="all, delete-orphan"
    )
    market_alerts: List[MarketAlert] = db.relationship(
        "MarketAlert", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return f"<User {self.email}.>"

    @classmethod
    def find_by_email(cls, email: str):
        """Find user by email."""
        return cls.query.filter_by(email=email).first()

    def set_password(self, password):
        """Set password for new user."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """Validate given password by user."""
        return bcrypt.check_password_hash(self.password, password)

    def confirm_user(self) -> None:
        """Set user as confirmed."""
        self.confirmed = True
        db.session.commit()

    def get_primary_portfolio(self) -> Portfolio:
        """Get primary portfolio."""
        return Portfolio.query.filter_by(user=self, primary=True).first()

    def add_portfolio(self, portfolio: Portfolio, save: bool = True) -> Portfolio:
        """Add new portfolio."""
        portfolio.user = self
        if save:
            portfolio.save_to_db()
        return portfolio

    def add_price_alert(self, security: Security, signal: MarketSignal) -> MarketAlert:
        """Add new price alert."""
        alert = MarketAlert(security=security, signal=signal, user=self)
        alert.save_to_db()
        return alert
