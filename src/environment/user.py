"""User"""
# pylint: disable=no-member, cyclic-import

from typing import List

from flask_login import UserMixin

from src.environment.base import BaseModel
from src.environment.portfolio import Portfolio
from src.environment.alerts import MarketAlert, WatchListInstrument
from src.extensions import db, bcrypt


class User(BaseModel, UserMixin):
    """Form a user class."""

    __tablename__ = "users"

    email: str = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password: str = db.Column(db.LargeBinary())
    confirmed: bool = db.Column(db.Boolean(), default=False)

    watch_list: List[WatchListInstrument] = db.relationship(
        "WatchListInstrument", back_populates="user", cascade="all, delete-orphan"
    )
    portfolios: List[Portfolio] = db.relationship(
        "Portfolio", back_populates="user", cascade="all, delete-orphan"
    )
    market_alerts: List[MarketAlert] = db.relationship(
        "MarketAlert", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, email: str, password: str, confirmed: bool = False) -> None:
        self.email = email
        self.set_password(password)
        self.confirmed = confirmed

    def __repr__(self):
        return f"<User {self.email}.>"

    @classmethod
    def find_by_email(cls, email: str) -> "User":
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
        self.commit()

    def get_primary_portfolio(self) -> Portfolio:
        """Get primary portfolio."""
        return Portfolio.query.filter_by(user=self, primary=True).first()

    def get_portfolio_by_name(self, name: str) -> Portfolio:
        """Get portfolio by name."""
        return Portfolio.query.filter_by(user=self, name=name).first()

    def add_portfolio(self, portfolio: Portfolio, save: bool = True) -> Portfolio:
        """Add new portfolio."""
        portfolio.user = self
        if save:
            portfolio.save_to_db()
        return portfolio

    def add_market_alert(self, alert: MarketAlert, save: bool = True) -> MarketAlert:
        """Add new price alert."""
        alert.user = self
        if save:
            alert.save_to_db()
        return alert

    def add_watchlist_instrument(
        self, instrument: WatchListInstrument, save: bool = True
    ) -> WatchListInstrument:
        """Add instrument to the watchlist."""
        instrument.user = self
        if save:
            instrument.save_to_db()
        return instrument
