import pytest

from src.utils import get_transactions_from_xlsx_file


@pytest.fixture
def test_transactions():
    return get_transactions_from_xlsx_file()
