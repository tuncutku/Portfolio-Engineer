position_dict = {
    "correct": [
        {
            "symbol": "Test Portfolio",
            "source": "Questrade",
            "quantity": 2,
            "state": "TFSA",
            "portfolio_id": 12345,
            "position_id": None,
        },
        {
            "symbol": "Test Portfolio",
            "source": "Questrade",
            "quantity": 345,
            "state": "TFSA",
            "portfolio_id": 12345,
            "position_id": 123,
        },
    ],
    "wrong": [
        {
            "symbol": "Test Portfolio",
            "source": "Questrade",
            "quantity": "Active",
            "state": "TFSA",
            "portfolio_id": 12345,
            "position_id": 123,
        },
    ],
}