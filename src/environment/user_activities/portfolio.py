import datetime

from src.environment.user_activities.base import BaseModel
from src.extensions import db
from src.market_data.yahoo import YFinance


class Currency:
    CAD = "CAD"
    USD = "USD"


class PortfolioType:
    tfsa = "TFSA"
    rrsp = "RRSP"
    margin = "Margin"
    cash = "Cash"
    custom = "Custom"


class PortfolioStatus:
    active = "Active"
    inactive = "Inactive"


class PortfolioSource:
    questrade = "Questrade"
    custom = "Custom"


class Portfolio(BaseModel):
    __tablename__ = "portfolios"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    name = db.Column(db.String(255), nullable=False)
    portfolio_type = db.Column(db.String(255), nullable=False)
    reporting_currency = db.Column(db.String(3), nullable=False)

    # Default attributes
    is_primary = db.Column(db.Boolean(), default=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)

    positions = db.relationship(
        "Position", backref="portfolio", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return "<Portfolio {}.>".format(self.name)

    @property
    def total_mkt_value(self) -> float:

        fx_md = YFinance("USDCAD=X")
        quote = fx_md.get_quote(decimal=2)

        value = 0
        for pos in self.positions:
            pos_mkt_cap = (
                pos.market_cap
                if pos.currency == self.reporting_currency
                else pos.market_cap * quote
            )
            value += pos_mkt_cap
        return value

    def edit(self, name, currency, port_type) -> None:
        self.name = name
        self.reporting_currency = currency
        self.portfolio_type = port_type
        db.session.commit()

    def set_as_primary(self) -> None:
        self.is_primary = True
        db.session.commit()

    def to_dict(self) -> dict:

        position_list = [position.to_dict() for position in self.positions]
        position_list.sort(key=lambda x: x.get("Market Cap"))

        return {
            "id": self.id,
            "Name": self.name,
            "Portfolio type": self.portfolio_type,
            "Reporting currency": self.reporting_currency,
            "Primary": self.is_primary,
            "Creation date": self.date,
            "Total market value": "{:,.2f}".format(self.total_mkt_value),
            "Positions": position_list,
        }

    # Questrade attributes
    # questrade_id = db.Column(db.Integer())
    # source = db.Column(db.String(255), default=PortfolioSource.custom)

    # def set_questrade_attributes(questrade_id):
    #     self.source = PortfolioSource.questrade
    #     self.questrade_id = questrade_id