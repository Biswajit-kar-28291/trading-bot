def place_and_format_order(client, symbol, side, order_type, quantity, price=None):
    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    summary = {
        "symbol": response.get("symbol"),
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "side": response.get("side"),
        "type": response.get("type"),
        "origQty": response.get("origQty"),
        "executedQty": response.get("executedQty"),
        "price": response.get("price"),
        "avgPrice": response.get("avgPrice", "N/A"),
    }
    return summary