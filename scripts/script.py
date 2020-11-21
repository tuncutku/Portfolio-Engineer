from lib.questrade import Questrade
from src.app.models.portfolio import Portfolio

("hello", "world") = (a for a in )

q = Questrade()

portfolioList = list()
accounts = q.accounts
portfolio_id = accounts["accounts"][0]["number"]

positions = q.account_positions(int(portfolio_id))
balances = q.account_balances(portfolio_id)
activities = q.account_activities(portfolio_id)
executions = q.account_executions(portfolio_id)
orders = q.account_orders(portfolio_id)


            