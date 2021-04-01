from src.environment.utils.base import Security
from datetime import date


class Equity(Security):
    __tablename__ = "equities"

    sector = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    business_summary = db.Column(db.String(255), nullable=False)


class ETF(Security):
    __tablename__ = "etfs"

    summary = db.Column(db.String(3), nullable=False)


class Option(Security):
    __tablename__ = "equity options"

    underlying_asset: Equity
    expiry = db.Column(db.DateTime, nullable=False)
    # datetime.fromtimestamp(1686873600)
    strike = db.Column(db.Float(), nullable=False)
    payoff: str
