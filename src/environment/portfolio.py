"""Portfolio"""
# pylint: disable=no-member, not-an-iterable, cyclic-import

from __future__ import annotations

from typing import List, TYPE_CHECKING
from datetime import datetime, date
from pandas import concat, DataFrame

from src.extensions import db

from src.environment.base import BaseModel
from src.environment.alerts import DailyReport
from src.environment.position import Position
from src.market import Security, Currency, Symbol, IndexValue, SingleValue
from src.market.ref_data import cad_ccy, gspc
from src.market.types import PortfolioType

if TYPE_CHECKING:
    from src.environment.user import User


class Portfolio(BaseModel):
    """Form a portfolio class."""

    __tablename__ = "portfolios"

    name: str = db.Column(db.String(255), nullable=False)
    portfolio_type: str = db.Column(db.String(255), nullable=False)
    reporting_currency: Currency = db.Column(db.PickleType(), nullable=False)
    benchmark: Security = db.Column(db.PickleType(), nullable=False)

    date: date = db.Column(db.Date(), default=datetime.now())
    primary: bool = db.Column(db.Boolean(), default=False)

    user: User = db.relationship("User", back_populates="portfolios")
    user_id: int = db.Column(db.Integer(), db.ForeignKey("users.id"))
    positions: List[Position] = db.relationship(
        Position, back_populates="portfolio", cascade="all, delete-orphan"
    )
    daily_report: DailyReport = db.relationship(
        "DailyReport",
        back_populates="portfolio",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        name: str,
        portfolio_type: str = PortfolioType.tfsa,
        reporting_currency: Currency = cad_ccy,
        benchmark: Security = gspc,
    ) -> None:

        self.name = name
        self.portfolio_type = portfolio_type
        self.reporting_currency = reporting_currency
        self.benchmark = benchmark

    def __repr__(self) -> str:
        return f"<Portfolio {self.name}.>"

    def position_values(
        self, start: date, end: date, currency: Currency = None
    ) -> DataFrame:
        """Get position historical values."""

        reporting_currency = currency or self.reporting_currency
        return concat(
            [
                position.historical_value(start, end, reporting_currency).index
                for position in self.positions
            ],
            axis=1,
        )

    def security_values(
        self, start: date, end: date, convert_currency=False
    ) -> DataFrame:
        """Get security historical values."""

        security_values = list()
        for position in self.positions:
            index = position.security.index(start, end)
            if convert_currency:
                index = index.to(self.reporting_currency)
            security_values.append(index.index)
        return concat(security_values, axis=1)

    def current_value(self, currency: Currency = None) -> SingleValue:
        """Current market value of the portfolio."""
        reporting_currency = currency or self.reporting_currency
        position_values = sum(
            [position.current_value(reporting_currency) for position in self.positions]
        )
        position_values.round(3)
        return position_values

    def historical_value(
        self, start: date, end: date = None, currency: Currency = None
    ) -> IndexValue:
        """Historical market value of the portfolio."""
        currency = currency or self.reporting_currency
        portfolio_value = self.position_values(start, end, currency).sum(axis=1)
        portfolio_value.rename(self.name, inplace=True)
        return IndexValue(portfolio_value, currency)

    def set_as_primary(self) -> None:
        """Check if a portfolio is set as primary."""
        self.primary = True
        db.session.commit()

    def edit(
        self, name: str, currency: Currency, port_type: str, benchmark: Security
    ) -> None:
        """Edit portfolio."""
        self.name = name
        self.reporting_currency = currency
        self.portfolio_type = port_type
        self.benchmark = benchmark
        db.session.commit()

    def get_positions_by_security_type(self, security_type) -> List[Position]:
        """Get position by security type."""
        return [
            position
            for position in self.positions
            if isinstance(position.security, security_type)
        ]

    def get_position_by_symbol(self, symbol: Symbol) -> Position:
        """Get position by symbol."""
        for position in self.positions:
            if position.security.symbol == symbol:
                return position
        return None

    def get_open_positions(self) -> List[Position]:
        """Get open positions."""
        return [position for position in self.positions if position.is_open]

    def add_position(self, position: Position, save: bool = True) -> Position:
        """Add new position."""
        position.portfolio = self
        if save:
            position.save_to_db()
        return position
