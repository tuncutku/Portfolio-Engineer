portofolio_dict = {
    "correct": [
        {
            "name": "Test Portfolio",
            "source": "Questrade",
            "status": "Active",
            "portfolio_type": "TFSA",
            "email": "test_email@gmail.com",
            "questrade_id": 12345,
            "portfolio_id": 123,
        },
        {
            "name": "Test Portfolio",
            "source": "Questrade",
            "status": "Active",
            "portfolio_type": "TFSA",
            "email": "test_email@gmail.com",
            "questrade_id": None,
            "portfolio_id": None,
        },
    ],
    "wrong": [
        {
            "name": "Test Portfolio",
            "source": "Questrade",
            "status": "Active",
            "portfolio_type": [1234],
            "email": "test_email@gmail.com",
            "questrade_id": "12345",
            "portfolio_id": "123",
        },
        {
            "name": None,
            "source": "Questrade",
            "status": "Active",
            "portfolio_type": "TFSA",
            "email": 111,
            "questrade_id": 1234,
            "portfolio_id": None,
        },
    ],
}