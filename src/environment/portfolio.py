# pylint: disable=no-member, not-an-iterable

from datetime import datetime, date
from typing import List

from src.extensions import db


from src.environment.utils.base import BaseModel
from src.environment.alerts.daily_report import DailyReport
from src.environment.position import Position
from src.environment.utils.types import *

from src.market import Observable, Currency, Symbol


class Portfolio(BaseModel):
    """Form a portfolio class."""

    __tablename__ = "portfolios"

    name: str = db.Column(db.String(255), nullable=False)
    portfolio_type: str = db.Column(db.String(255), nullable=False)
    reporting_currency: Currency = db.Column(db.PickleType(), nullable=False)
    benchmark: Symbol = db.Column(db.PickleType(), nullable=False)

    date: date = db.Column(db.Date(), default=datetime.now())
    primary: bool = db.Column(db.Boolean(), default=False)

    user_id: int = db.Column(db.Integer(), db.ForeignKey("users.id"))
    positions: List[Position] = db.relationship(
        Position, backref="portfolio", cascade="all, delete-orphan"
    )
    daily_report: DailyReport = db.relationship(
        "DailyReport",
        back_populates="portfolio",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Portfolio {self.name}.>"

    @classmethod
    def get_primary(cls, user):
        return cls.query.filter_by(user=user, primary=True).first()

    def set_as_primary(self) -> None:
        """Check if a portfoli is set as primary."""
        self.primary = True
        db.session.commit()

    def edit(self, name, currency, port_type, benchmark) -> None:
        """Edit portfolio."""
        self.name = name
        self.reporting_currency = currency
        self.portfolio_type = port_type
        self.benchmark = benchmark
        db.session.commit()

    def get_position_by_symbol(self, symbol) -> Position:
        """Get position by symbol."""
        [position for position in self.positions]

    def add_position(self, security: Observable) -> Position:
        """Add new position."""
        position = Position(security=security, portfolio=self)
        position.save_to_db()
        return position

    @property
    def total_mkt_value(self) -> float:
        """Total market value of the portfolio including all asset classes."""
