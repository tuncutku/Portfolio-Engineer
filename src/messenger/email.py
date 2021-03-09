from pydantic.dataclasses import dataclass
import pandas as pd
from datetime import datetime
from typing import List

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.environment.utils.types import *


class Email(BaseModel):
    pass