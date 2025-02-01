import pandas as pd

from src.utils import (get_transactions_for_period,
                       get_transactions_from_xlsx_file, get_user_settings)


def test_get_user_settings():
    settings = get_user_settings()
    assert isinstance(settings, dict)
    assert "user_currencies" in settings
    assert "user_stocks" in settings
    assert settings["user_currencies"] == ["USD", "EUR"]
    assert settings["user_stocks"] == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def test_get_transactions_from_xlsx_file():
    transactions = get_transactions_from_xlsx_file()
    assert isinstance(transactions, pd.DataFrame)
    assert not transactions.empty
    assert "Дата операции" in transactions.columns
    assert "Категория" in transactions.columns
    assert "Сумма операции" in transactions.columns
    assert "Кэшбэк" in transactions.columns
    assert "Номер карты" in transactions.columns
    assert "Описание" in transactions.columns


def test_get_transactions_for_period():
    date_from = pd.to_datetime("2021-09-01")
    date_to = pd.to_datetime("2021-10-01")
    transactions = get_transactions_for_period(date_from, date_to)
    assert isinstance(transactions, pd.DataFrame)
    assert not transactions.empty
    assert "Дата операции" in transactions.columns
    assert "Категория" in transactions.columns
    assert "Сумма операции" in transactions.columns
    assert "Кэшбэк" in transactions.columns
