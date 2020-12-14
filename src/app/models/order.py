from dataclasses import dataclass
from typing import List

from src.db import database
from lib.questrade import Questrade

@dataclass
class Order:
    order_id: int
    symbol: int