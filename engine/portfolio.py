from engine import costs


class Portfolio:
    """Holds cash and Bitcoin. Long-only: either all cash or all Bitcoin."""

    def __init__(self, starting_cash):
        self.cash = starting_cash
        self.units = 0.0          # amount of BTC held
        self.entry_cost = 0.0     # cash spent to open the current position

    def in_position(self):
        return self.units > 0

    def buy(self, open_price):
        """Spend ALL cash on BTC, at a slightly worse price, paying the fee."""
        price = costs.buy_price(open_price)
        fee = costs.fee(self.cash)
        self.units = (self.cash - fee) / price
        self.entry_cost = self.cash
        self.cash = 0.0
        return {"action": "BUY", "price": price, "units": self.units, "fee": fee}

    def sell(self, open_price):
        """Sell ALL BTC, at a slightly worse price, paying the fee."""
        price = costs.sell_price(open_price)
        proceeds = self.units * price
        fee = costs.fee(proceeds)
        self.cash = proceeds - fee
        profit = self.cash - self.entry_cost
        trade = {"action": "SELL", "price": price, "units": self.units,
                 "fee": fee, "profit": profit}
        self.units = 0.0
        self.entry_cost = 0.0
        return trade

    def equity(self, price):
        """Total account value at a given price: cash plus Bitcoin."""
        return self.cash + self.units * price