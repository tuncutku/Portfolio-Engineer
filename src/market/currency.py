from pydantic import BaseModel


currency_coverage = ["USD", "CAD", "EUR", "TRY"]


class Currency(BaseModel):
    """Form a currency object from a string."""

    currency: str
