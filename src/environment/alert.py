from src.environment.utils.base import AlertBaseModel
from src.environment.utils.types import AlertPeriod


class DailyReport(AlertBaseModel):
    period = AlertPeriod.TradingDaysDaily

    def condition(self):
        return True

    @property
    def email_template(self):
        pass


class TechnicalAlert(AlertBaseModel):
    period = AlertPeriod.TradingDaysEvery5Min

    def condition(self):
        return True

    @property
    def email_template(self):
        pass


class NewsAlert(AlertBaseModel):
    period = AlertPeriod.TradingDaysEvery5Min

    def condition(self):
        return True

    @property
    def email_template(self):
        pass


class EconomicAlert(AlertBaseModel):
    period = AlertPeriod.TradingDaysEvery5Min

    def condition(self):
        return True

    @property
    def email_template(self):
        pass
