import json
import time
import requests
import configparser
from flask import session
from dataclasses import dataclass

from src.db import DB_Token
from src.questrade.utils import (
    TokenNotFoundError,
    InvalidTokenError,
    InternalServerError,
)

from flask_login import current_user


@dataclass
class Auth(object):

    config: configparser.ConfigParser

    @property
    def token(self):
        return self._read_valid_token()

    def _read_valid_token(self):
        """ Function to check if previous access token is still valid. If not, use refresh token to claim a new access token. """
        self.token_data = self._read_token()
        if self.token_data is None:
            raise TokenNotFoundError("Currently no token found.")
        if time.time() + 60 > int(self.token_data["expires_at"]):
            self._refresh_token(self.token_data["refresh_token"])
            self.token_data = self._read_token()
        return self.token_data

    def _refresh_token(self, refresh_token: str):
        req_time = int(time.time())
        payload = requests.get(self.config["Auth"]["RefreshURL"].format(refresh_token))
        if payload.status_code == 200:
            token = payload.json()
            token["expires_at"] = str(req_time + token["expires_in"])
            if self._read_token() is None:
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