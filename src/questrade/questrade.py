import requests
import os
import inspect
import pandas as pd
from datetime import datetime, timedelta
from functools import wraps
from abc import ABCMeta, abstractmethod

from src.questrade.utils import _read_config
from src.questrade.utils import InvalidTokenError
from src.questrade.auth import Auth

CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "questrade.cfg")


class Questrade(metaclass=ABCMeta):
    def __init__(self):
        self.session = requests.Session()
        self.config = _read_config(CONFIG_PATH)
        self.auth = Auth(self.config)

    
    @classmethod
    def _call_api_on_func(cls, func):
        """ Decorator for forming the api call with the arguments of the
        function, it works by taking the arguments given to the function
        and building the url to call the api on it
        Keyword Arguments:
            func:  The function to be decorated
        """
        argspec = inspect.getfullargspec(func)
        try:
            positional_count = len(argspec.args) - len(argspec.defaults)
            defaults = dict(
                zip(argspec.args[positional_count:], argspec.defaults))
        except:
            if argspec.args:
                # No defaults
                positional_count = len(argspec.args)
                defaults = {}
            elif argspec.defaults:
                # Only defaults
                positional_count = 0
                defaults = argspec.defaults
        
        @wraps(func)
        def _call_wrapper(self, *args, **kwargs):
            endpoint, params = func(self, *args, **kwargs)
            return self._request(endpoint, params)
        return _call_wrapper
    
    # @classmethod
    # def _output_format(cls, output_format: str):
    #     def _output_decorator(func):
    #         """ Decorator in charge of giving the output its right format, either
    #         json or pandas
    #         Keyword Arguments:
    #             func:  The function to be decorated
    #             override:  Override the internal format of the call, default None
    #         """
    #         @wraps(func)
    #         def _format_wrapper(self, *args, **kwargs):
    #             call_response = func(self, *args, **kwargs)
    #             if call_response.status_code == 401:
    #                 raise InvalidTokenError("Wrong token provided, access denied. Please update the token.")
    #             if output_format == "json":
    #                 return call_response.json()
    #             elif output_format == "pandas":
    #                 return pd.json_normalize(call_response)
    #         return _format_wrapper
    #     return _output_decorator


    def access_status(self) -> bool:
        self.time

    def submit_refresh_token(self, refresh_token):
        self.auth._refresh_token(refresh_token)

    def _request(self, endpoint, params: dict = None):
        token = self.auth.token
        # set headers
        headers = {"Authorization": token["token_type"] + " " + token["access_token"]}
        self.session.headers.update(headers)

        # generate url for the request
        url = token["api_server"] + "v1" + endpoint

        resp = self.session.request("get", url, params=params, timeout=30)
        if resp.status_code == 401:
            raise InvalidTokenError("Wrong token provided, access denied. Please update the token.")
        return resp.json()

    @property
    def _now(self):
        return datetime.now().astimezone().isoformat("T")

    def _days_ago(self, d):
        now = datetime.now().astimezone()
        return (now - timedelta(days=d)).isoformat("T")
