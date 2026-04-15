import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import place_and_format_order
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logger


def build_parser():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders only")
    return parser


def main():
    load_dotenv()
    logger = setup_logger()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        print("Error: Missing API credentials in .env")
        sys.exit(1)

    parser = build_parser()
    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)

        print("\nOrder Request Summary")
        print("-" * 30)
        print(f"Symbol     : {symbol}")
        print(f"Side       : {side}")
        print(f"Order Type : {order_type}")
        print(f"Quantity   : {quantity}")
        print(f"Price      : {price if price else 'N/A'}")

        client = BinanceFuturesClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            logger=logger
        )

        result = place_and_format_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        print("\nOrder Response")
        print("-" * 30)
        for k, v in result.items():
            print(f"{k:12}: {v}")

        print("\nSuccess: Order placed successfully.")

    except ValueError as e:
        logger.error("Validation error: %s", e)
        print(f"Validation Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unhandled error")
        print(f"Failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()