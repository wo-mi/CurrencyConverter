import requests
import json


class Api:
    @staticmethod
    def request(currency_code, date, cache):
        date_str = date.strftime("%Y-%m-%d")

        api_url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/{date_str}/"

        try:
            response = requests.get(api_url)
        except Exception:
            raise ConnectionError("Connection to API failed")

        if response.status_code == 200:
            json_str = json.dumps(response.json())
            cache.put(currency_code, date, json_str)
            return json_str

        elif response.status_code == 404:
            cache.put(currency_code, date, None)
            return None

        elif response.status_code == 400:
            return None

        else:
            raise ConnectionError("Connection to API failed")
