"""Portfolio"""
# pylint: disable=no-member, not-an-iterable, cyclic-import

from typing import List
from datetime import datetime, date
from pandas import concat, DataFrame

from src.extensions import db

from src.environment.base import BaseModel
from src.environment.alerts import DailyReport
from src.environment.position import Position
from src.market import Security, Currency, Symbol, IndexValue


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

    def position_values(self, start: date, end: date) -> DataFrame:
        """Get position historical values."""

        return concat(
            [
                position.historical_value(self.reporting_currency, start, end).index
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

    @property
    def current_value(self):
        """Current market value of the portfolio."""
        value = sum(
            [
                position.current_value(self.reporting_currency)
                for position in self.positions
            ]
        )
        value.round(3)
        return value

    def historical_value(self, start: date, end: date = None) -> IndexValue:
        """Historical market value of the portfolio."""
        portfolio_value = self.position_values(start, end).sum(axis=1)
        portfolio_value.rename(self.name, inplace=True)
        return IndexValue(portfolio_value, self.reporting_currency)

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

    def get_positions_by_security(self, security_type) -> List[Position]:
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

    def add_position(self, security: Security) -> Position:
        """Add new position."""
        position = Position(security=security, portfolio=self)
        position.save_to_db()
        return position
