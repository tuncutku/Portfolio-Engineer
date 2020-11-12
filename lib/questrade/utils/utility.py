import logging
import yaml
import os
import configparser


def _read_config(fpath):
        config = configparser.ConfigParser()
        with open(os.path.expanduser(fpath)) as f:
            config.read_file(f)
        return config

def _validate_access_token(
    access_token=None,
    api_server=None,
    expires_in=None,
    refresh_token=None,
    token_type=None,
):
    """Validate access token
    This function validates the access token and ensures that all requiered
    attributes are provided.
    Parameters
    ----------
    access_token: str, optional
        Access token
    api_server: str, optional
        Api server URL
    expires_in: int, optional
        Time until token expires
    refresh_token: str, optional
        Refresh token
    token_type: str, optional
        Token type
    Raises
    ------
    Exception
        If any of the inputs is None.
    """
    if access_token is None:
        raise Exception("Access token was not provided.")
    if api_server is None:
        raise Exception("API server URL was not provided.")
    if expires_in is None:
        raise Exception("Expiry time was not provided.")
    if refresh_token is None:
        raise Exception("Refresh token was not provided.")
    if token_type is None:
        raise Exception("Token type was not provided.")