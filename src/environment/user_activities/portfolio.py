from pydantic.dataclasses import dataclass
from typing import List

from src.db import DB_Portfolio
from src.environment.user_activities.utils import (
    credential_check, 
    UserAlreadyRegisteredError, 
    UserNotFoundError, 
    InvalidEmailError, 
    IncorrectPasswordError, 
    PortfolioNotFoundError,
)

@dataclass
class Portfolio:
    name: str
    source: str
    status: str
    portfolio_type: str
    email: str
    questrade_id: int = None
    portfolio_id: int = None

    @classmethod
    def find_all(cls, email: str) -> List["Portfolio"]:
        port_list = DB_Portfolio.get_portfolio_list(email)
        return [cls(*port) for port in port_list]

    @classmethod
    def find_by_name(cls, name: str, email: str) -> "Portfolio":
        port = DB_Portfolio.get_portfolio(name, email)
        return cls(*port)

    @staticmethod
    def add_portfolio(name: str, source: str, status: str, portfolio_type: str, email: str, questrade_id: int = None) -> None:
        DB_Portfolio.add_portfolio(name, source, status, portfolio_type, email, questrade_id)
    
    def update_portfolio(self, name: str, status: str, portfolio_type: str) -> None:
        DB_Portfolio.update_portfolio(name, status, portfolio_type, self.portfolio_id)
    
    def delete_portfolio(self) -> None:
        DB_Portfolio.delete_portfolio(self.portfolio_id)




    