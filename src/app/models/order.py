from dataclasses import dataclass
from typing import List

from src.app.db import database
from src.app.lib.questrade import Questrade

@dataclass
class Order:
    order_id: int
    symbol: int