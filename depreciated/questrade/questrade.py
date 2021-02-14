import requests
import os
import inspect
from datetime import datetime, timedelta
from functools import wraps
from abc import ABCMeta
import json
import time
import requests
import configparser
from flask import session
from src.questrade.utils import (
    TokenNotFoundError,
    InvalidTokenError,
    InternalServerError,
)

from flask_login import current_user


from src.questrade.utils import _read_config
from src.questrade.utils import InvalidTokenError

CONFIG_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "questrade.cfg")


class Questrade(metaclass=ABCMeta):
    def __init__(self):
        self.session = requests.Session()
        self.config = _read_config(CONFIG_PATH)

    @classmethod
    def _call_api_on_func(cls, func):
        """Decorator for forming the api call with the arguments of the
        function, it works by taking the arguments given to the function
        and building the url to call the api on it
        Keyword Arguments:
            func:  The function to be decorated
        """

        @wraps(func)
        def _call_wrapper(self, *args, **kwargs):
            endpoint, params = func(self, *args, **kwargs)
            return self._request(endpoint, params)

        return _call_wrapper

    def _request(self, endpoint, params: dict = None):
        token = self.read_valid_token()
        # set headers
        headers = {"Authorization": token["token_type"] + " " + token["access_token"]}
        self.session.headers.update(headers)

        # generate url for the request
        url = token["api_server"] + "v1" + endpoint

        resp = self.session.request("get", url, params=params, timeout=30)
        if resp.status_code == 401:
            raise InvalidTokenError(
                "Wrong token provided, access denied. Please update the token."
            )
        return resp.json()

    def read_valid_token(self):
        """ Function to check if previous access token is still valid. If not, use refresh token to claim a new access token. """
        self.token_data = current_user.questrade_access_token
        if self.token_data is None:
            raise TokenNotFoundError("Currently no token found.")
        if time.time() + 60 > int(self.token_data["expires_at"]):
            self._refresh_token(self.token_data["refresh_token"])
            self.token_data = current_user.questrade_access_token
        return self.token_data

    def refresh_token(self, refresh_token: str):
        req_time = int(time.time())
        payload = requests.get(self.config["Auth"]["RefreshURL"].format(refresh_token))
        if payload.status_code == 200:
            token = payload.json()
            token["expires_at"] = str(req_time + token["expires_in"])
            if current_user.questrade_access_token is None:
                self._write_token(token)
            else:
                self._update_token(token)
        elif payload.status_code == 500:
            raise InternalServerError(
                "Cannot acces to Questrade, internal server error."
            )
        else:
            raise InvalidTokenError(
                "Wrong token provided, access denied. Please update the token."
            )

    def _read_token(self):
        return DB_Token.find_token_by_user_email(current_user.email)

    def _write_token(self, token):
        DB_Token.add_user_token(
            token["access_token"],
            token["api_server"],
            token["expires_at"],
            token["refresh_token"],
            token["token_type"],
            current_user.email,
        )

    def _update_token(self, token):
        DB_Token.update_user_token(
            token["access_token"],
            token["api_server"],
            token["expires_at"],
            token["refresh_token"],
            token["token_type"],
            current_user.email,
        )

    @property
    def _now(self):
        return datetime.now().astimezone().isoformat("T")

    def _days_ago(self, d):
        now = datetime.now().astimezone()
        return (now - timedelta(days=d)).isoformat("T")