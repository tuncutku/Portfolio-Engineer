from lib.questrade import Questrade
from src.app.models.portfolio import Portfolio

q = Questrade()

portfolioList = list()
accounts = q.accounts
for account in accounts["accounts"]:
    portfolio = Portfolio(
        account["type"],
        account["number"],
        account["status"],
        account["clientAccountType"],
        accounts["userId"]
    )
    portfolioList.append(portfolio)
            