from abc import ABC, abstractmethod
from dataclasses import dataclass
from flask import session

@dataclass
class Model(ABC):

    def __post_init__(self):
        self.user_email = session.get("email")

    @classmethod
    @abstractmethod
    def get_from_questrade(cls):
        pass

    @classmethod
    @abstractmethod
    def get_from_db(csl):
        pass

    @abstractmethod
    def write_to_db(cls):
        pass

    @abstractmethod
    def update_db(cls):
        pass
