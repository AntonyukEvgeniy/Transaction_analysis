from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.decorators import log, log_result_to_file
from src.utils import get_transactions_from_xlsx_file


@log("log.txt")
@log_result_to_file(filename="output.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        now = datetime.now()
    else:
        now = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    transactions["date"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    date_from = now - relativedelta(months=3)
    filtered_transactions = transactions.loc[
        (transactions["Категория"] == category) & (transactions["date"] >= date_from)
    ]
    spending = filtered_transactions.groupby("Категория", as_index=False)["Сумма операции"].sum(-1)
    spending["Сумма операции"] = spending["Сумма операции"].apply(lambda x: -1 * x)
    return spending


if __name__ == "__main__":
    data_1 = get_transactions_from_xlsx_file()
    result = spending_by_category(data_1, category="Переводы", date="22.12.2021 21:40:59")
    print(result)
