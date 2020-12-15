import requests
import os
from datetime import datetime, timedelta

from src.services.questrade.utils import _read_config
from src.models.auth import Auth

CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "questrade.cfg")


class Questrade:
    def __init__(self):
        self.session = requests.Session()
        self.config = _read_config(CONFIG_PATH)
        self.auth = Auth(self.config)

    def access_status(self) -> bool:
        self.time

    def submit_refresh_token(self, refresh_token):
        self.auth._refresh_token(refresh_token)

    def _request(self, endpoint, params: dict = None, request: str = "get"):
        token = self.auth.token
        # set headers
        headers = {"Authorization": token["token_type"] + " " + token["access_token"]}
        self.session.headers.update(headers)

        # generate url for the request
        url = token["api_server"] + "v1" + endpoint

        resp = self.session.request(request, url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    @property
    def _now(self):
        return datetime.now().astimezone().isoformat("T")

    def _days_ago(self, d):
        now = datetime.now().astimezone()
        return (now - timedelta(days=d)).isoformat("T")

    @property
    def time(self):
        return self._request(self.config["API"]["time"])

    @property
    def accounts(self):
        return self._request(self.config["API"]["Accounts"])

    def account_positions(self, id):
        return self._request(self.config["API"]["AccountPositions"].format(id))

    def account_balances(self, id):
        return self._request(self.config["API"]["AccountBalances"].format(id))

    def account_executions(self, id, **kwargs):
        return self._request(self.config["API"]["AccountExecutions"].format(id), kwargs)

    def account_orders(self, id, **kwargs):
        """Get account orders
        Parameters:
            id (int): Account Id
            kwargs: startTime, endTime, ids
            
        Returns:
            list: orders
        """
        if "ids" in kwargs:
            kwargs["ids"] = kwargs["ids"].replace(" ", "")
        return self._request(self.config["API"]["AccountOrders"].format(id), kwargs)

    def account_order(self, id, order_id):
        return self._request(self.config["API"]["AccountOrder"].format(id, order_id))

    def account_activities(self, id, **kwargs):
        if "startTime" not in kwargs:
            kwargs["startTime"] = self._days_ago(1)
        if "endTime" not in kwargs:
            kwargs["endTime"] = self._now
        return self._request(self.config["API"]["AccountActivities"].format(id), kwargs)

    def symbol(self, id):
        return self._request(self.config["API"]["Symbol"].format(id))

    def symbols(self, **kwargs):
        if "ids" in kwargs:
            kwargs["ids"] = kwargs["ids"].replace(" ", "")
        return self._request(self.config["API"]["Symbols"].format(id), kwargs)

    def symbols_search(self, **kwargs):
        return self._request(self.config["API"]["SymbolsSearch"].format(id), kwargs)

    def symbol_options(self, id):
        return self._request(self.config["API"]["SymbolOptions"].format(id))

    @property
    def markets(self):
        return self._request(self.config["API"]["Markets"])

    def markets_quote(self, id):
        return self._request(self.config["API"]["MarketsQuote"].format(id))

    def markets_quotes(self, **kwargs):
        if "ids" in kwargs:
            kwargs["ids"] = kwargs["ids"].replace(" ", "")
        return self._request(self.config["API"]["MarketsQuotes"], kwargs)

    def markets_options(self, **kwargs):
        return self._request(self.config["API"]["MarketsOptions"], kwargs)

    def markets_strategies(self, **kwargs):
        return self._request(self.config["API"]["MarketsStrategies"], kwargs)

    def markets_candles(self, id, **kwargs):
        if "startTime" not in kwargs:
            kwargs["startTime"] = self._days_ago(1)
        if "endTime" not in kwargs:
            kwargs["endTime"] = self._now
        return self._request(self.config["API"]["MarketsCandles"].format(id), kwargs)