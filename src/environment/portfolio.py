"""Portfolio"""
# pylint: disable=no-member, not-an-iterable, cyclic-import

from __future__ import annotations

from typing import List, TYPE_CHECKING
from datetime import datetime
from pandas import concat, DataFrame

from src.extensions import db

from src.environment.base import BaseModel
from src.environment.alerts import DailyReport
from src.environment.position import Position
from src.market import Instrument, Currency, Symbol, IndexValue, SingleValue, Info
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
    benchmark: Instrument = db.Column(db.PickleType(), nullable=False)

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
        benchmark: Instrument = gspc,
    ) -> None:

        self.name = name
        self.portfolio_type = portfolio_type
        self.reporting_currency = reporting_currency
        self.benchmark = benchmark

    def __repr__(self) -> str:
        return f"<Portfolio {self.name}.>"

    def position_quantities(self, start: date, end: date) -> DataFrame:
        """Get position historical quantities."""
        return concat(
            [
                position.cumulative_quantity_index(start, end)
                for position in self.positions
            ],
            axis=1,
        )

    def security_values(
        self, start: date, end: date, currency: Currency = None
    ) -> DataFrame:
        """Get security historical values."""
        return concat(
            [
                position.security_historical_value(start, end, currency).index
                for position in self.positions
            ],
            axis=1,
        )

    def position_values(
        self, start: date, end: date, currency: Currency = None
    ) -> DataFrame:
        """Get position historical values."""

        values = self.security_values(start, end, currency)
        quantities = self.position_quantities(start, end)
        return values * quantities

    def current_value(
        self, currency: Currency = None, request: str = Info.price
    ) -> SingleValue:
        """Current market value of the portfolio."""
        reporting_currency = currency or self.reporting_currency
        position_values = [
            position.current_value(reporting_currency, request)
            for position in self.positions
        ]
        return round(sum(position_values), 3)

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
        self.commit()

    def edit(
        self, name: str, currency: Currency, port_type: str, benchmark: Instrument
    ) -> None:
        """Edit portfolio."""
        self.name = name
        self.reporting_currency = currency
        self.portfolio_type = port_type
        self.benchmark = benchmark
        self.commit()

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

    def get_security_sector_info(self) -> dict:
        """Get basic information of the underlying instruments."""
        positions = self.get_open_positions()
        sectors = dict()
        for position in positions:
            sectors[position.security.symbol.symbol] = position.security.sector
        return sectors

    def optimizer(self, start, end):
        """Get optimizer."""
