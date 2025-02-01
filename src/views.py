import json
from datetime import datetime, time, timedelta
from typing import Any, Dict, List, Union

import pandas as pd

from src.decorators import log
from src.external_api import get_currency_rates, get_stock_rates
from src.utils import get_transactions_for_period, get_user_settings


@log("log.txt")
def greetings(curr_time: time) -> str:
    """
    Приветствие в формате
    "???"
    , где
    ???
    «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
    """
    hour = curr_time.hour
    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        raise ValueError("Unexpected hour value")


@log("log.txt")
def cards_widget(transactions_for_period: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    По каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей).
    """
    summed_df = transactions_for_period.groupby("Номер карты", as_index=False)["Сумма операции"].sum()
    cards = []
    for _, row in summed_df.iterrows():
        if row["Номер карты"] != "":
            last_digits = str.replace(row["Номер карты"], "*", "")
            total_spent = round(-1 * row["Сумма операции"], 2)
            cards.append({"last_digits": last_digits, "total_spent": total_spent})
    return cards


@log("log.txt")
def top_trans_by_payment(transactions_for_period: pd.DataFrame) -> List[Dict[str, float]]:
    """
    Топ-5 транзакций по сумме платежа
    """
    transactions_sorted_by_payment = transactions_for_period.sort_values(by="Сумма платежа").head(5)
    top_five = []
    for _, row in transactions_sorted_by_payment.iterrows():
        top_five.append(
            {
                "date": row["Дата платежа"],
                "amount": -1 * row["Сумма платежа"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    return top_five


@log("log.txt")
def get_rates() -> List[Dict[str, float]]:
    """
    Возвращает курс валют в рублях. Пример:
    {'user_currencies': ['USD', 'EUR'], 'user_stocks': ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']}
    """
    user_currencies = get_user_settings()["user_currencies"]
    currency_rates = get_currency_rates(curr_symbols=user_currencies)
    return currency_rates


@log("log.txt")
def get_stock_prices() -> list[dict[str, Union[str, float]]]:
    """
    Возвращает стоимость акций из S&P500 в рублях.
    """
    user_stocks = get_user_settings()["user_stocks"]
    stock_prices = get_stock_rates(stock_symbols=user_stocks)
    return stock_prices


@log("log.txt")
def main_page(current_date: str) -> str:
    """
    Принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающую JSON-ответ. В ответе содержаться все данные необходимые для отображения главной страницы.
    """
    curr_date = datetime.strptime(current_date, "%Y-%m-%d %H:%M:%S")
    start_date = datetime(curr_date.year, curr_date.month, 1)
    end_date = datetime(curr_date.year, curr_date.month, curr_date.day) + timedelta(days=1)
    curr_time = curr_date.time()
    greeting = greetings(curr_time)
    transactions_for_period = get_transactions_for_period(start_date, end_date)
    cards = cards_widget(transactions_for_period)
    top_five_trans_by_payment = top_trans_by_payment(transactions_for_period)
    currency_rates = get_rates()
    stock_prices = get_stock_prices()
    result_data = {
        "greetings": greeting,
        "cards": cards,
        "top_five_trans": top_five_trans_by_payment,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    result_data_json = json.dumps(result_data, ensure_ascii=False)
    return result_data_json


if __name__ == "__main__":
    curr_date = datetime.strptime("2021-12-15 00:00:00", "%Y-%m-%d %H:%M:%S")
    start_date = datetime(curr_date.year, curr_date.month, 1)
    end_date = datetime(curr_date.year, curr_date.month, curr_date.day) + timedelta(days=1)
    curr_time = curr_date.time()
    result = greetings(curr_time)
    print(result)
