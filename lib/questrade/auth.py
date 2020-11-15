
import os
import json
import time
import requests
import yaml

TOKEN_PATH = ("access_token.yml")

class Auth:
    def __init__(self, config, session, refresh_path):
        self.token_path = TOKEN_PATH
        self.config = config
        self.session = session
        self.refresh_path = refresh_path
    
    @property
    def token(self):
        return self._read_valid_token()

    def _read_token(self):
        with open(self.token_path) as yaml_file:
            token_yaml_payload = yaml.safe_load(yaml_file)
        return token_yaml_payload
    
    def _read_valid_token(self):
        """ Function to check if previous access token is still valid. If not, use refresh token to claim a new access token. """
        self.token_data = self._read_token()
        if time.time() + 60 < int(self.token_data["expires_at"]):
            return self.token_data
        else:
            self._refresh_token(self.token_data["refresh_token"])
            self.token_data = self._read_token()
            return self.token_data

    def _refresh_token(self, refresh_token):
        req_time = int(time.time())
        payload = requests.get(self.config["Auth"]["RefreshURL"].format(refresh_token))
        if payload.status_code == 200:
            token = payload.json()
            token["expires_at"] = str(req_time + token["expires_in"])
            self._write_token(token)
        
    # TODO Token is stored in a yml file. It could be stored as an environment variable    
    def _write_token(self, token):
        with open(self.token_path, "w") as yaml_file:
            yaml.dump(token, yaml_file)
