import json
import requests
from config import exchanger


class ConverterException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise ConverterException('неверное количество параметров')
        quote, base, amount = values

        if quote == base:
            raise ConverterException(f' Невозможно перевести одинаковые валюты {base}')
        try:
            quote_formatted = exchanger[quote]
        except KeyError:
            raise ConverterException(f' Не удалось обработать валюту {quote}')
        try:
            base_formatted = exchanger[base]
        except KeyError:
            raise ConverterException(f' Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException(f' Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_formatted}&symbols={base_formatted}')
        res = float(json.loads(r.content)['rates'][base_formatted]) * amount
        return round(res, 3)