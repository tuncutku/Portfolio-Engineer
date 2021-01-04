import logging
import yaml
import os
import configparser


def _read_config(fpath):
        config = configparser.ConfigParser()
        with open(os.path.expanduser(fpath)) as f:
            config.read_file(f)
        return config
