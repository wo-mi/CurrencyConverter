import sys
import argparse
from datetime import datetime


class Parser:
    def parse(self):
        argument_parser = argparse.ArgumentParser()
        required_arguments = argument_parser.add_argument_group("required arguments")
        required_arguments.add_argument(
            "-a", metavar="AMOUNT", type=self._amount_validate, required=True, help="amount in origin currency"
        )
        required_arguments.add_argument(
            "-f", metavar="FROM", type=self._currency_validate, required=True, help="origin currency code (ISO 4217)"
        )
        required_arguments.add_argument(
            "-t", metavar="TO", type=self._currency_validate, required=True, help="target currency code (ISO 4217)"
        )
        required_arguments.add_argument(
            "-d", metavar="DATE", type=self._date_validate, required=True, help="exchange date (YYYY-MM-DD)"
        )

        args = argument_parser.parse_args()

        amount = args.a
        origin_currency_code = args.f
        target_currency_code = args.t
        date = args.d

        if origin_currency_code == target_currency_code:
            raise ValueError("Currencies shouldn't be the same.")

        return (amount, origin_currency_code, target_currency_code, date)

    def _amount_validate(self, string):
        try:
            value = float(string)
        except ValueError:
            raise argparse.ArgumentTypeError("Invalid float value")

        if value < 0:
            raise argparse.ArgumentTypeError("Not positive value")
        else:
            return value

    def _currency_validate(self, string):
        if string.upper() not in [
            "THB",
            "USD",
            "AUD",
            "HKD",
            "CAD",
            "NZD",
            "SGD",
            "EUR",
            "HUF",
            "CHF",
            "GBP",
            "UAH",
            "JPY",
            "CZK",
            "DKK",
            "ISK",
            "NOK",
            "SEK",
            "HRK",
            "RON",
            "BGN",
            "TRY",
            "ILS",
            "CLP",
            "PHP",
            "MXN",
            "ZAR",
            "BRL",
            "MYR",
            "IDR",
            "INR",
            "KRW",
            "CNY",
            "XDR",
        ]:
            raise argparse.ArgumentTypeError("Currency value error")

        else:
            return string.upper()

    def _date_validate(self, string):
        try:
            dt = datetime.strptime(string, "%Y-%m-%d")
        except ValueError:
            raise argparse.ArgumentTypeError("Invalid date")

        if dt > datetime.now():
            raise argparse.ArgumentTypeError("Date can't be later than today")

        return dt.date()
