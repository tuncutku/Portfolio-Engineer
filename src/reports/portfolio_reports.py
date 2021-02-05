from src.environment.user_activities.portfolio import Portfolio
from src.environment.user_activities.order import Order
from src.environment.user_activities.position import Position
import pandas as pd
import yfinance as yf
import inspect


class PortfolioReport:
    def __init__(self, portfolio: Portfolio, start_date=None, end_date=None):
        self.underlying_portfolio = portfolio

    def generate_position_df(self):
        order_list = Order.query.filter_by(
            portfolio_id=self.underlying_portfolio.id
        ).all()
        return pd.DataFrame.from_records([order.to_dict() for order in order_list])

    @property
    def positions(self):
        df = self.generate_position_df()

        position_list = list()
        for symbol in df.symbol.unique():
            symbol_df = df.loc[df["symbol"] == symbol]

            symbol_info = yf.Ticker(symbol).info
            position_attr = [
                "symbol",
                "shortName",
                "quoteType",
                "currency",
            ]
            position_attr_dict = dict()
            for attr in position_attr:
                position_attr_dict[attr] = symbol_info.get(attr, None)
            position_list.append(Position.from_dict(**position_attr_dict))
        return position_list

    @property
    def position_attributes_map(self):
        return Position.position_attributes_map()
