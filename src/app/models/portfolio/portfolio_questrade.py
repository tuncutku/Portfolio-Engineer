from dataclasses import dataclass
from typing import List

from src.db import database
from src.app.models.utils import credential_check, UserAlreadyRegisteredError, UserNotFoundError, InvalidEmailError, IncorrectPasswordError
from lib.questrade import Questrade

@dataclass
class QuestradePortfolio:
    _id: str
    user: str
    q: Questrade



    @property
    def positions(self) -> List[dict]:
        return self.q.account_positions(int(self._id))["positions"]
    
    @property
    def balances(self) -> dict:
        return self.q.account_balances(int(self._id))

    @property
    def activities(self):
        # activities = q.account_activities(int(portfolio_id))
        pass

    @property
    def executions(self):
        # executions = q.account_executions(portfolio_id)
        pass

    @property
    def order(self):
        # TODO return a class of 
        # order = q.account_order(orders[0])
        pass

@dataclass
class QuestradePortfolio:
    _id = str


    