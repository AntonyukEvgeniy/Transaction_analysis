import json
import os
from dotenv import load_dotenv
import requests


def convert_into_rubles(*, transaction: dict) -> float:
    """
    Принимает на вход транзакцию. Возвращает сумму, указанною в транзакции.
    Если сумма транзакции указана не в рублях(а в USD или EUR), конвертирует сумму в рубли.
    Курсы конвертации валют получает обращаясь к стороннему API:
    https://apilayer.com/marketplace/exchangerates_data-api#endpoints
    """
    amount = transaction["operationAmount"]["amount"]
    currency_source_code = transaction["operationAmount"]["currency"]["code"]
    if currency_source_code == "USD" or currency_source_code == "EUR":
        load_dotenv()
        api_key = os.getenv("API_KEY")
        currency_target_code = "RUB"
        url = "https://api.apilayer.com/exchangerates_data/convert"
        payload = {"amount": amount, "from": currency_source_code, "to": currency_target_code}
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers, params=payload)
        status_code = response.status_code
        result = response.json()
        if status_code != 200:
            raise Exception("Что-то пошло не так!")
        rounded_amount = round(result["result"], 2)
        return float(rounded_amount)
    else:
        return float(amount)

def get_stock_rates(*, stock_symbols: [str]) -> list[dict]:
    load_dotenv()
    api_key = os.getenv("API_KEY_STOCKS")
    url = 'https://www.alphavantage.co/query'
    stock_prices = []
    for stock_symbol in stock_symbols:
        payload = {"function": "TIME_SERIES_DAILY", "symbol": stock_symbol,"apikey": api_key}
        response = requests.get(url,  params=payload)
        status_code = response.status_code
        if status_code != 200:
            raise Exception("Что-то пошло не так!")
        data = response.json()
        last_refresh = data["Meta Data"]["3. Last Refreshed"]
        price = data["Time Series (Daily)"][last_refresh]["4. close"]
        rounded_price = round(float(price), 2)
        stock_prices.append({"stock": stock_symbol, "price": rounded_price})
    return stock_prices


def get_currency_rates(*, curr_symbols: [str]) -> list[dict]:
    load_dotenv()
    api_key = os.getenv("API_KEY_CURRENCIES")
    currency_rates = []
    symbols = ','.join(curr_symbols)
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
        rate = round(1/data["rates"][symbol],2)
        currency_rates.append({"currency":symbol,"rate":rate})
    return currency_rates

if __name__ == '__main__':
    # curr_symbols = ["USD", "EUR"]
    # result = get_currency_rates(curr_symbols = curr_symbols)
    stock_symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    result = get_stock_rates(stock_symbols=stock_symbols)
    print(result)