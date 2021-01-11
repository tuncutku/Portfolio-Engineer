from src.questrade.questrade import Questrade
from src.questrade.utils import InvalidSymbolError

class Questrade_Market_Data(Questrade):

    @staticmethod
    def get_symbol_id(raw_symbols: list, position_symbol: str):
        if not raw_symbols:
            raise InvalidSymbolError("Invalid Symbol!")
        for index, raw_symbol in enumerate(raw_symbols["symbols"]):
            if raw_symbol["symbol"] == position_symbol:
                return raw_symbol["symbolId"]
        raise InvalidSymbolError("Invalid Symbol!")


    @Questrade._call_api_on_func
    def symbol(self, id):
        return (self.config["API"]["Symbol"].format(id), None)

    @Questrade._call_api_on_func
    def symbols(self, **kwargs):
        if "ids" in kwargs:
            kwargs["ids"] = kwargs["ids"].replace(" ", "")
        return self._request(self.config["API"]["Symbols"].format(id), kwargs)

    @Questrade._call_api_on_func
    def symbols_search(self, **kwargs):
        return (self.config["API"]["SymbolsSearch"].format(id), kwargs)

    @Questrade._call_api_on_func
    def symbol_options(self, id):
        return (self.config["API"]["SymbolOptions"].format(id), None)

    @property
    @Questrade._call_api_on_func
    def markets(self):
        return (self.config["API"]["Markets"], None)

    @Questrade._call_api_on_func
    def markets_quote(self, id):
        return (self.config["API"]["MarketsQuote"].format(id), None)

    @Questrade._call_api_on_func
    def markets_quotes(self, **kwargs):
        if "ids" in kwargs:
            kwargs["ids"] = kwargs["ids"].replace(" ", "")
        return (self.config["API"]["MarketsQuotes"], kwargs)

    @Questrade._call_api_on_func
    def markets_options(self, **kwargs):
        return (self.config["API"]["MarketsOptions"], kwargs)

    @Questrade._call_api_on_func
    def markets_strategies(self, **kwargs):
        return (self.config["API"]["MarketsStrategies"], kwargs)

    @Questrade._call_api_on_func
    def markets_candles(self, id, **kwargs):
        if "startTime" not in kwargs:
            kwargs["startTime"] = self._days_ago(1)
        if "endTime" not in kwargs:
            kwargs["endTime"] = self._now
        return (self.config["API"]["MarketsCandles"].format(id), kwargs)                                                                                                                                                                                                                                     