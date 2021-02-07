from src.environment.user_activities.portfolio import Portfolio
from src.environment.user_activities.order import Order
from src.environment.user_activities.position import Position
import pandas as pd
import yfinance as yf
import inspect


class PortfolioReport:
    def __init__(self, portfolio: Portfolio, start_date=None, end_date=None):
        self.underlying_portfolio = portfolio
        self.positions = self.get_positions()

    def generate_order_df(self):
        order_list = Order.query.filter_by(
            portfolio_id=self.underlying_portfolio.id
        ).all()
        return pd.DataFrame.from_records([order.to_dict() for order in order_list])

    @property
    def port_mkt_cap():
        pass

    def get_positions(self):
        position_list = list()
        df = self.generate_order_df()
        if not df.empty:
            df["Side multiplier"] = df["side"].apply(lambda x: 1 if x == "Buy" else -1)
            df["Side amount"] = df["Side multiplier"] * df["quantity"]

            position_list = list()
            for symbol in df.symbol.unique():
                symbol_df = df.loc[df["symbol"] == symbol]
                position_list.append(Position.from_df(symbol, df))
        return position_list

    @property
    def position_attributes_map(self):
        return Position.position_attributes_map()

    @property
    def total_portfolio_value(self):
        pass
