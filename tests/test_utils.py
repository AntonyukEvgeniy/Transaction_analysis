from datetime import datetime

import pandas as pd
import pytest

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


@pytest.fixture
def mock_transactions():
    num_days = (datetime(2022, 12, 31) - datetime(2021, 1, 1)).days + 1
    return pd.DataFrame({
        "Дата операции": pd.date_range(start="2021-01-01", periods=num_days, freq='D'),
        "Сумма операции": [-100] * num_days,
        "Категория": ["Test"] * num_days
    })


def test_get_transactions_for_period(mock_transactions, monkeypatch):
    def mock_get_transactions():
        return mock_transactions

    monkeypatch.setattr("src.utils.get_transactions_from_xlsx_file", mock_get_transactions)

    date_from = datetime(2021, 12, 1)
    date_to = datetime(2021, 12, 16)
    result = get_transactions_for_period(date_from, date_to)

    assert not result.empty
    assert "Дата операции" in result.columns
