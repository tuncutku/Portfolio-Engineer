from dataclasses import dataclass

from src.app.lib.questrade import Questrade
from src.app.db import database
from src.app.models.utils import credential_check, UserAlreadyRegisteredError, UserNotFoundError, InvalidEmailError, IncorrectPasswordError
from src.app.models.auth import Auth

@dataclass
class User(object):
    email: str
    password: str  
    
    @classmethod
    def find_by_email(cls, email: str) -> "User":
        user = database.find_user_by_email(email)
        if user:
            return cls(*user)
        else:
            raise UserNotFoundError("A user with this e-mail was not found.")

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: The password
        :return: True if valid, an exception otherwise
        """
        user = cls.find_by_email(email)
        if not credential_check.check_hashed_password(password, user.password):
            raise IncorrectPasswordError("Your password was wrong.")
        return True

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        """
        This method registers a user using e-mail and password.
        :param email: user's e-mail (might be invalid)
        :param password: password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        if not credential_check.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")
        try:
            user = cls.find_by_email(email)
            raise UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        except UserNotFoundError:
            database.add_user(email, credential_check.hash_password(password))
        return True

    @staticmethod
    def logout():
        pass

    
    @staticmethod
    def portfolio_list(q: Questrade):
        portfolioList = list()
        accounts = q.accounts
        for account in accounts["accounts"]:
            portfolio = {
                "port_type": account["type"],
                "number": account["number"],
                "status": account["status"],
                "account_type": account["clientAccountType"],
                "userId": accounts["userId"],
            }
            portfolioList.append(portfolio)
        return portfolioList
