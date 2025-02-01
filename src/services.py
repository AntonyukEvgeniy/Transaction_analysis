import json

import pandas as pd

from src.decorators import log
from src.utils import get_transactions_from_xlsx_file


@log("log.txt")
def get_favorable_categories(data, year, month):
    """
    На вход функции поступают данные для анализа, год и месяц.
    На выходе — JSON с анализом, сколько на каждой категории можно заработать кэшбэка в указанном месяце года.
    """
    data["date"] = pd.to_datetime(data["Дата операции"], dayfirst=True)
    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.month
    filtered_data = data.loc[(data["month"] == month) & (data["year"] == year)]
    cashback_by_category = filtered_data.groupby("Категория", as_index=False)["Кэшбэк"].sum()
    cashback_by_category = cashback_by_category.sort_values(by=["Кэшбэк"], ascending=False)
    cashback_by_category_dict = dict(zip(cashback_by_category["Категория"], cashback_by_category["Кэшбэк"]))
    cashback_by_category_json = json.dumps(cashback_by_category_dict, ensure_ascii=False)
    return cashback_by_category_json


if __name__ == "__main__":
    data_1 = get_transactions_from_xlsx_file()
    result = get_favorable_categories(data_1, 2021, 10)
    print(result)
