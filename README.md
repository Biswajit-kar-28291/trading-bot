# Binance Futures Testnet Trading Bot

A simple Python CLI bot for placing MARKET and LIMIT orders on Binance Futures Testnet (USDT-M).

## Features
- Place MARKET and LIMIT orders
- Supports BUY and SELL
- CLI input validation
- Structured project layout
- Logs API requests, responses, and errors
- Error handling for invalid input, API failures, and network issues

## Tech Stack
- Python 3
- requests
- argparse
- python-dotenv
- logging

## Setup
1. Create and activate a Binance Futures Testnet account
2. Generate API key and secret
3. Create `.env` file:

```env
BINANCE_API_KEY=EDVPmYtoLdG38HcMFxPjlnmH2mcyiJ6kHgBE371wG55OLn1CDdpIS9eRnSBlNKRp
BINANCE_API_SECRET=VRLtNaBlSJStK2ZaxqVkw8O7Ql2zFlaCnAvG3Ufl3anIUzs2ckyqEhzK8ZAFxTYA
BINANCE_BASE_URL=https://testnet.binancefuture.com