import json

from src.services import get_favorable_categories


def test_get_favorable_categories(test_transactions):
    year = 2021
    month = 10
    result = get_favorable_categories(test_transactions, year, month)
    assert isinstance(result, str)

    # Verify the JSON structure
    cashback_data = json.loads(result)
    assert isinstance(cashback_data, dict)
    assert all(isinstance(category, str) for category in cashback_data.keys())
