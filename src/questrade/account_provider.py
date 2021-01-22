from src.questrade.questrade import Questrade


class Questrade_Account(Questrade):
    @property
    @Questrade._call_api_on_func
    def time(self):
        return (self.config["API"]["time"], None)

    @property
    @Questrade._call_api_on_func
    def accounts(self):
        return (self.config["API"]["Accounts"], None)

    @Questrade._call_api_on_func
    def account_positions(self, id):
        return (self.config["API"]["AccountPositions"].format(id), None)

    @Questrade._call_api_on_func
    def account_balances(self, id):
        return (self.config["API"]["AccountBalances"].format(id), None)

    @Questrade._call_api_on_func
    def account_executions(self, id, **kwargs):
        return (self.config["API"]["AccountExecutions"].format(id), kwargs)

    @Questrade._call_api_on_func
    def account_orders(self, id, **kwargs):
        """Get account orders
        Parameters:
            id (int): Account Id
            kwargs: startTime, endTime, ids

        Returns:
            list: orders
        """
        if "ids" in kwargs:
            kwargs["ids"] = kwargs["ids"].replace(" ", "")
        return (self.config["API"]["AccountOrders"].format(id), kwargs)

    @Questrade._call_api_on_func
    def account_order(self, id, order_id):
        return (self.config["API"]["AccountOrder"].format(id, order_id), None)

    @Questrade._call_api_on_func
    def account_activities(self, id, **kwargs):
        if "startTime" not in kwargs:
            kwargs["startTime"] = self._days_ago(1)
        if "endTime" not in kwargs:
            kwargs["endTime"] = self._now
        return (self.config["API"]["AccountActivities"].format(id), kwargs)