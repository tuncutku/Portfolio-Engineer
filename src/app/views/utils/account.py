import random

from src.app.models.portfolio import Portfolio

def check_and_update_portfolio(port_db: Portfolio, port_questrade: dict) -> None:
    """Utility function that checks if Questrade portfolio is up-to-date. If not, updates database."""

    check_list = [
        port_db.portfolio_type == port_questrade["type"],
        port_db.status == port_questrade["status"],
    ]

    if not all(check_list):
        Portfolio.update_portfolio(
            port_questrade["status"],
            port_questrade["type"], 
            port_db.name,
        )

def add_portfolio(port_questrade: dict, email: str) -> None:
    """Add a questrade portfolio with randon name"""

    # Find a valid name
    valid_name = False
    while valid_name == False:
        n_port = random.randrange(1, 1000)
        port_name = f"My Questrade Portfolio {n_port}"
        valid_name = _valide_portfolio_name(port_name, email)

    Portfolio.add_portfolio(
        port_name,
        "Questrade",
        port_questrade["status"],
        port_questrade["type"],
        email,
        int(port_questrade["number"])
    )

def _valide_portfolio_name(name, email) -> bool:
    name_list = [port.name for port in Portfolio.find_all(email)]
    return name not in name_list
