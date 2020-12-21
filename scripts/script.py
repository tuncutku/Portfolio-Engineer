from src.questrade import Questrade
#from src.environment.user_activities.portfolio import Portfolio
import redis

from datetime import datetime, timedelta

start_time = {"startTime" : datetime(2019,8,1)}

from cryptography.fernet import Fernet

key = Fernet.generate_key()

r = redis.Redis(
    host='hostname',
    port=port,
    password='password'
)


q = Questrade()

portfolioList = list()
q.time
accounts = q.accounts
portfolio_id = accounts["accounts"][0]["number"]



p = Portfolio(portfolio_id, q)
p.positions
p.balances


positions = q.account_positions(int(portfolio_id))
balances = q.account_balances(portfolio_id)
activities = q.account_activities(int(portfolio_id))
executions = q.account_executions(portfolio_id)
orders = q.account_orders(portfolio_id, startTime=(datetime.now().astimezone() - timedelta(days=600)).isoformat("T"), stateFilter="All")


            