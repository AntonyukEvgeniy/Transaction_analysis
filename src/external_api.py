import os
from typing import Dict, List, Union

import requests
from dotenv import load_dotenv

from src.decorators import log

load_dotenv()


@log("log.txt")
def get_stock_rates(*, stock_symbols: list[str]) -> list[dict[str, Union[str, float]]]:
    """
    Возвращает стоимость акций по переданным символам.

    :param stock_symbols: список символов акций
    :return: список словарей c символом акции и ее стоимостью
    """
    api_key = os.getenv("API_KEY_STOCKS")
    url = "https://www.alphavantage.co/query"
    stock_prices = []
    for stock_symbol in stock_symbols:
        payload = {"function": "TIME_SERIES_DAILY", "symbol": stock_symbol, "apikey": api_key}
        response = requests.get(url, params=payload)
        status_code = response.status_code
        if status_code != 200:
            raise Exception("Что-то пошло не так!")
        data = response.json()
        last_refresh = data["Meta Data"]["3. Last Refreshed"]
        price = data["Time Series (Daily)"][last_refresh]["4. close"]
        rounded_price = round(float(price), 2)
        stock_prices.append({"stock": stock_symbol, "price": rounded_price})
    return stock_prices


@log("log.txt")
def get_currency_rates(*, curr_symbols: list[str]) -> List[Dict[str, float]]:
    """
    Получает валютные курсы для указанных валютных символов относительно рубля.

    :param curr_symbols: список символов валют
    :return: список словарей с символом валюты и её курсом
    """
    api_key = os.getenv("API_KEY_CURRENCIES")
    currency_rates = []
    symbols = ",".join(curr_symbols)
    base_currency = "RUB"
    url = "https://api.apilayer.com/exchangerates_data/latest"
    payload = {"symbols": symbols, "base": base_currency}
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers, params=payload)
    status_code = response.status_code
    if status_code != 200:
        raise Exception("Что-то пошло не так!")
    data = response.json()
    for symbol in curr_symbols:
        rate = round(1 / data["rates"][symbol], 2)
        currency_rates.append({"currency": symbol, "rate": rate})
    return currency_rates


if __name__ == "__main__":
    # curr_symbols = ["USD", "EUR"]
    # result = get_currency_rates(curr_symbols = curr_symbols)
    stock_symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    result = get_stock_rates(stock_symbols=stock_symbols)
    print(result)
