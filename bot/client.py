import time
import hmac
import hashlib
from urllib.parse import urlencode

import requests


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str, logger):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _sign_params(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, path: str, params=None, signed=False):
        params = params or {}
        url = f"{self.base_url}{path}"

        if signed:
            params = self._sign_params(params)

        self.logger.info("API Request | %s %s | params=%s", method, url, params)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                timeout=15
            )

            self.logger.info(
                "API Response | status=%s | body=%s",
                response.status_code,
                response.text
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            self.logger.error("HTTP error: %s | body=%s", e, response.text if response else "")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error("Network error: %s", e)
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price=None):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "recvWindow": 5000,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._request("POST", "/fapi/v1/order", params=params, signed=True)