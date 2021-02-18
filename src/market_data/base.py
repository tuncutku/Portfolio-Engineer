from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError, validator


class BaseProvider(ABC):
    @property
    @abstractmethod
    def is_valid(self):
        pass

    @property
    @abstractmethod
    def underlying_company(self):
        pass

    @abstractmethod
    def get_company_info(self):
        pass

    @abstractmethod
    def get_company_financials(self):
        pass