"""Sample request data"""

from datetime import date

start_date = date(2020, 1, 2).strftime("%Y-%m-%d")

successful_alerts = [
    dict(signal="Price Signal", underlying="AAPL", operator="Up", target=130),
    dict(signal="Daily Return Signal", underlying="AAPL", operator="Up", target=0.05),
    dict(
        signal="Limit Return Signal",
        underlying="AAPL",
        operator="Up",
        target=0.05,
        start_date=start_date,
    ),
    dict(
        signal="Portfolio Value Signal",
        underlying="portfolio_1",
        operator="Up",
        target=1300,
    ),
    dict(
        signal="Daily Portfolio Return Signal",
        underlying="portfolio_1",
        operator="Up",
        target=0.05,
    ),
]
