import pandas as pd

from src.reports import spending_by_category
from src.utils import get_transactions_from_xlsx_file


def test_spending_by_category():
    data = get_transactions_from_xlsx_file()
    result = spending_by_category(data, category="Переводы", date="22.12.2021 21:40:59")
    expected = pd.DataFrame([{"Категория": "Переводы", "Сумма операции": 64335.92}])
    pd.testing.assert_frame_equal(result, expected)
