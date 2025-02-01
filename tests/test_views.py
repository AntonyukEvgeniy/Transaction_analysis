import json
from datetime import datetime

import pandas as pd
import pytest

from src.utils import get_transactions_from_xlsx_file
from src.views import (cards_widget, get_rates, get_stock_prices, greetings,
                       main_page, top_trans_by_payment)


@pytest.mark.parametrize("current_date, expected_greeting", [
    (datetime(2021, 12, 15, 14, 49), "Добрый день"),
    (datetime(2021, 1, 1), "Доброй ночи"),
    (datetime(2022, 6, 1, 12, 0), "Добрый день"),
])
def test_main_page(current_date, expected_greeting, monkeypatch):
    expected_cards = [{"last_digits": "1234", "total_spent": 1000}, {"last_digits": "5678", "total_spent": 2000}]
    expected_top_five_trans = [{"date": "2021-12-15", "amount": 500, "category": "test", "description": "test"}]
    expected_currency_rates = [{"currency": "USD", "rate": 78.0}, {"currency": "EUR", "rate": 85.0}]
    expected_stock_prices = [{"stock": "AAPL", "price": 100.0}, {"stock": "AMZN", "price": 2000.0}]

    def mock_get_transactions_from_xlsx_file():
        return pd.DataFrame({"date": [current_date.strftime("%d.%m.%Y")], "amount": [1000], "category": ["test"]})

    def mock_cards_widget(transactions):
        return expected_cards

    def mock_top_trans_by_payment(transactions):
        return expected_top_five_trans

    def mock_get_currency_rates(curr_symbols):
        return expected_currency_rates

    def mock_get_stock_prices():
        return expected_stock_prices

    monkeypatch.setattr("src.views.get_transactions_from_xlsx_file", mock_get_transactions_from_xlsx_file)
    monkeypatch.setattr("src.views.cards_widget", mock_cards_widget)
    monkeypatch.setattr("src.views.top_trans_by_payment", mock_top_trans_by_payment)
    monkeypatch.setattr("src.views.get_currency_rates", mock_get_currency_rates)
    monkeypatch.setattr("src.views.get_stock_prices", mock_get_stock_prices)

    result = main_page(current_date.strftime("%Y-%m-%d %H:%M:%S"))
    assert isinstance(result, str)
    data = json.loads(result)
    assert "greetings" in data
    assert data["greetings"] == expected_greeting
    assert "cards" in data
    assert data["cards"] == expected_cards
    assert "top_five_trans" in data
    assert data["top_five_trans"] == expected_top_five_trans
    assert "currency_rates" in data
    assert data["currency_rates"] == expected_currency_rates
    assert "stock_prices" in data
    assert data["stock_prices"] == expected_stock_prices


@pytest.fixture
def mock_get_currency_rates(monkeypatch):
    currency_rates = [
        {"currency": "USD", "rate": 78.0},
        {"currency": "EUR", "rate": 85.0},
    ]

    def mock_get_currency_rates(*args, **kwargs):
        return currency_rates

    monkeypatch.setattr("src.views.get_currency_rates", mock_get_currency_rates)


def test_get_rates(mock_get_currency_rates):
    result = get_rates()
    assert isinstance(result, list)
    assert len(result) == 2
    assert set(result[0].keys()) == {"currency", "rate"}
    assert set(result[1].keys()) == {"currency", "rate"}


@pytest.fixture
def mock_get_stock_prices(monkeypatch):
    stock_prices = [
        {"stock": "AAPL", "price": 100.0},
        {"stock": "AMZN", "price": 2000.0},
        {"stock": "GOOGL", "price": 3000.0},
        {"stock": "MSFT", "price": 400.0},
        {"stock": "TSLA", "price": 500.0},
    ]

    def mock_get_stock_rates(*args, **kwargs):
        return stock_prices

    monkeypatch.setattr("src.views.get_stock_rates", mock_get_stock_rates)


def test_get_stock_prices(mock_get_stock_prices):
    result = get_stock_prices()
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(isinstance(stock, dict) for stock in result)
    assert all("stock" in stock for stock in result)
    assert all("price" in stock for stock in result)


@pytest.mark.parametrize("hour, expected_greeting", [
    (0, "Доброй ночи"),
    (6, "Доброе утро"),
    (12, "Добрый день"),
    (18, "Добрый вечер"),
    (23, "Добрый вечер"),
])
def test_greetings(hour, expected_greeting):
    curr_time = datetime.strptime(f"{hour}:00", "%H:%M").time()
    result = greetings(curr_time)
    assert isinstance(result, str)
    assert result == expected_greeting


def test_cards_widget():
    result = cards_widget(get_transactions_from_xlsx_file())
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(card, dict) for card in result)
    assert all("last_digits" in card for card in result)
    assert all("total_spent" in card for card in result)


def test_top_trans_by_payment():
    result = top_trans_by_payment(get_transactions_from_xlsx_file())
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(trans, dict) for trans in result)
    assert all("category" in trans for trans in result)
    assert all("amount" in trans for trans in result)
