"""Yahoo"""

import json
import re

import requests

_DEFAULT_PARAMS = {
    "lang": "en-US",
    "corsDomain": "finance.yahoo.com",
    ".tsrc": "finance",
}


class Yahoo:
    """Yahoo provider"""

    def get_info(self, symbol: str):
        """Get info."""

        url = "https://finance.yahoo.com/quote"
        ticker_url = "{}/{}".format(url, symbol)
        response = requests.get(ticker_url, params=self.params(symbol), timeout=30).text

        json_str = (
            response.split("root.App.main =")[1]
            .split("(this)")[0]
            .split(";\n}")[0]
            .strip()
        )
        data = json.loads(json_str)["context"]["dispatcher"]["stores"][
            "QuoteSummaryStore"
        ]

        # return data
        new_data = json.dumps(data).replace("{}", "null")
        new_data = re.sub(r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", new_data)

        return json.loads(new_data)

    @staticmethod
    def params(symbol) -> dict:
        """Parameters to use in API calls"""
        # Construct the code request string.
        params = {"symbols": symbol}
        params.update(_DEFAULT_PARAMS)
        return params


yf = Yahoo()
yf.get_info("AAPL")
