# pylint: disable=no-member, not-an-iterable

from datetime import datetime, date
from typing import List
from pandas import concat

from src.extensions import db


from src.environment.utils.base import BaseModel
from src.environment.alerts.daily_report import DailyReport
from src.environment.position import Position
from src.environment.utils.types import *

from src.market import Security, Currency, Symbol


class Portfolio(BaseModel):
    """Form a portfolio class."""

    __tablename__ = "portfolios"

    name: str = db.Column(db.String(255), nullable=False)
    portfolio_type: str = db.Column(db.String(255), nullable=False)
    reporting_currency: Currency = db.Column(db.PickleType(), nullable=False)
    benchmark: Security = db.Column(db.PickleType(), nullable=False)

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
        """Get the primary portfolio."""
        return cls.query.filter_by(user=user, primary=True).first()

    @property
    def current_value(self):
        """Current market value of the portfolio."""
        return sum(
            [
                position.current_value(self.reporting_currency)
                for position in self.positions
            ]
        )

    def historical_value(self, start: date, end: date = None):
        """Historical market value of the portfolio."""
        return sum(
            [
                position.historical_value(self.reporting_currency, start, end)
                for position in self.positions
            ]
        )

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

    def get_positions_by_security(self, Security_type) -> List[Position]:
        """Get position by security type."""
        return [
            position
            for position in self.positions
            if isinstance(position.security, Security_type)
        ]

    def get_position_by_symbol(self, symbol: Symbol) -> Position:
        """Get position by symbol."""
        for position in self.positions:
            if position.security.symbol == symbol:
                return position
        return

    def add_position(self, security: Security) -> Position:
        """Add new position."""
        position = Position(security=security, portfolio=self)
        position.save_to_db()
        return position
