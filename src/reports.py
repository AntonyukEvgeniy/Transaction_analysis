from datetime import datetime
from typing import Optional
import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import get_transactions_from_xlsx_file


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date = datetime.today().date()
    curr_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    transactions['date'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)
    date_from = curr_date - relativedelta(months=3)
    filtered_transactions = transactions.loc[(transactions['Категория']==category) & (transactions['date'] >= date_from)]
    spending = filtered_transactions.groupby('Категория', as_index=False)['Сумма операции'].sum(-1)
    spending['Сумма операции'] = spending['Сумма операции'].apply(lambda x: -1*x)
    return spending

if __name__ == '__main__':
    data_1 = get_transactions_from_xlsx_file()
    result = spending_by_category(data_1,category="Супермаркеты",date ="31.12.2021 16:44:00")
    print(result)
