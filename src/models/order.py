from dataclasses import dataclass
from typing import List

from src.db import database
from src.services.questrade import Questrade

@dataclass
class Order:
    symbol: str
    quantity: int
    portfolio_id: str
    position_id: int

    order_id: int




	"totalQuantity":  100,
	"openQuantity":  100,
	"filledQuantity":  0,
	"canceledQuantity": 0,
	"side": "Buy",
	"type": "Limit",
	"limitPrice": 500.95,
	"stopPrice": null,
	"icebergQty": null,
	"minQuantity": null,
	"avgExecPrice": null,
	"lastExecPrice": null,
	"gtdDate":  null,
	"state": "Canceled",
	"creationTime": 2014-10-23T20:03:41.636000-04:00,
	"updateTime": 2014-10-23T20:03:42.890000-04:00,
	"comissionCharged": 0,
	"isInsider":  false,
	"isLimitOffsetInDollar": false,
	"placementCommission":  null,
	"legs": [],
	"strategyType": "SingleLeg",
	"triggerStopPrice": null,0

    executionFee
    Double
    Liquidity fee charged by execution venue.
    secFee
    Double
    SEC fee charged on all sales of US securities.
    canadianExecutionFee
    Integer
    Additional execution fee charged by TSX (if applicable).

    @classmethod
    def find_all(cls):
        pass

    @classmethod
    def find_by_id(cls):
        pass

    @classmethod
    def generate_by_orders(cls, orders: list):
        pass

    def add_position():
        pass





