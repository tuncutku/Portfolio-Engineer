from dataclasses import dataclass
from typing import List

from src.db import DB_Portfolio
from src.models.utils import (
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
    portfolio_id: int
    questrade_id: int = None

    @classmethod
    def find_all(cls, email: str) -> List["Portfolio"]:
        port_list = DB_Portfolio.get_portfolio_list(email)
        if port_list is None:
            raise PortfolioNotFoundError("No portfolio exist in the database. Add a custom portfolio or update with Questrade.")
        return [cls(*port) for port in port_list]

    @classmethod
    def find_by_name(cls, name: str, email: str) -> "Portfolio":
        DB_Portfolio.get_portfolio(name, email)

    @staticmethod
    def add_portfolio(name: str, source: str, status: str, portfolio_type: str, email: str, portfolio_id: int) -> None:
        DB_Portfolio.add_portfolio(name, source, status, portfolio_type, email, portfolio_id)
    
    @staticmethod
    def update_portfolio(status: str, portfolio_type: str, name: str) -> None:
        DB_Portfolio.update_portfolio(status, portfolio_type, name)
    
    def delete(self) -> None:
        DB_Portfolio.delete_portfolio(self.email, self.name)




    