import json
from CurrencyConverter import Converter, Parser, AWS


def main():
    parser = Parser()
    amount, origin_currency_code, target_currency_code, date = parser.parse()

    converter = Converter()
    result = converter.convert(amount, origin_currency_code, target_currency_code, date)

    aws = AWS()
    aws.append_data(result)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
