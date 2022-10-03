import json
from datetime import datetime, timedelta
from .cache import Cache
from .api import Api


class Converter:
    def __init__(self):
        self._cache = Cache()

    def convert(self, amount, origin_currency_code, target_currency_code, date):
        origin_currency_rate = None
        target_currency_rate = None
        exchange_date = date

        # Verify only 10 days back.
        # Prevent infinity loop in case of incorrect API responde
        for i in range(10):
            origin_currency_rate = self._get_currancy_rate(origin_currency_code, exchange_date)
            target_currency_rate = self._get_currancy_rate(target_currency_code, exchange_date)

            if origin_currency_rate is not None and target_currency_rate is not None:
                break
            else:
                exchange_date = exchange_date - timedelta(days=1)

        if origin_currency_rate <= 0 and target_currency_rate <= 0:
            raise ValueError("Currency rate can't be lower than or equal to 0")

        rate_between_currencies = origin_currency_rate / target_currency_rate

        target_amount = round(amount * rate_between_currencies, 4)

        result = {
            "origin_amount": amount,
            "origin_currency_code": origin_currency_code,
            "target_amount": target_amount,
            "target_currency_code": target_currency_code,
            "exchange_date": exchange_date.strftime("%Y-%m-%d"),
        }

        return result

    def _get_currancy_rate(self, currency_code, date):
        response_json_str = None
        cache_response_json_str = self._cache.get(currency_code, date)

        if cache_response_json_str != False:
            response_json_str = cache_response_json_str
        else:
            response_json_str = Api.request(currency_code, date, self._cache)

        if response_json_str is not None:
            rate = self._get_rate_from_json_str(response_json_str)
            return rate
        else:
            return None

    def _get_rate_from_json_str(self, json_str):
        try:
            j = json.loads(json_str)
            return j["rates"][0]["mid"]

        except Exception as e:
            raise Exception("Can't parse json.")
