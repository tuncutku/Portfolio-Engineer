from dataclasses import dataclass
from typing import List

from src.db import database
from src.models.utils import credential_check, UserAlreadyRegisteredError, UserNotFoundError, InvalidEmailError, IncorrectPasswordError, PortfolioNotFoundError
from src.services.questrade import Questrade

@dataclass
class Portfolio:
    name: str
    source: str
    status: str
    portfolio_type: str
    email: str
    portfolio_id: int
    questrade_id: int = None

    @classmethod
    def find_all(cls, email: str) -> List["Portfolio"]:
        port_list = database.get_portfolio_list(email)
        if port_list is None:
            raise PortfolioNotFoundError("No portfolio exist in the database. Add a custom portfolio or update with Questrade.")
        return [cls(*port) for port in port_list]

    @classmethod
    def find_by_name(cls, name: str, email: str) -> "Portfolio":
        database.get_portfolio(name, email)

    @staticmethod
    def add_portfolio(name: str, source: str, status: str, portfolio_type: str, email: str, portfolio_id: int) -> None:
        database.add_portfolio(name, source, status, portfolio_type, email, portfolio_id)
    
    @staticmethod
    def update_portfolio(status: str, portfolio_type: str, name: str) -> None:
        database.update_portfolio(status, portfolio_type, name)
    
    def delete(self) -> None:
        database.delete_portfolio(self.email, self.name)


    @property
    def tags(self):
        """Porperty that generates tags from orders which will be used for filtering news."""
        pass

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
    def orders(self):
        # TODO return a list of Order class
        # order = q.account_order(orders[0])
        pass



    