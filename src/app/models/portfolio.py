from dataclasses import dataclass

from src.db import database
from src.app.models.utils import credential_check, UserAlreadyRegisteredError, UserNotFoundError, InvalidEmailError, IncorrectPasswordError


@dataclass
class Portfolio:
    accountType: str
    number: str
    status: str
    clientAccountType: str
    userId: int
 
    