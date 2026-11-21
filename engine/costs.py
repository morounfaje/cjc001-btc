import config


def buy_price(open_price, slippage=config.SLIPPAGE):
    """Price actually paid when buying: slightly higher than the open."""
    return open_price * (1 + slippage)


def sell_price(open_price, slippage=config.SLIPPAGE):
    """Price actually received when selling: slightly lower than the open."""
    return open_price * (1 - slippage)


def fee(trade_value, fee_rate=config.FEE_RATE):
    """Fee charged on the dollar value of a trade."""
    return trade_value * fee_rate