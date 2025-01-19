from pathlib import Path
from typing import Any
import pandas as pd
import json
from pandas import DataFrame

OPERATIONS_PATH = "data/operations.xlsx"
SETTINGS_PATH = "user_settings.json"

def file(filepath: str) -> Path:
    data_folder = Path(__file__).parent.parent
    file_to_open = data_folder / filepath
    return file_to_open

def get_transactions_from_xlsx_file(filepath: str = OPERATIONS_PATH) -> DataFrame:
    """
    Принимает на вход путь до exel-файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    try:
        file_to_open = file(filepath)
        excel_data = pd.read_excel(file_to_open)
        # logger.debug(f"Файл {file_to_open} успешно прочитан")
        return excel_data
    except Exception as e:
        # logging.error(e)
        raise e

def get_transactions_for_period(date_from, date_to) -> DataFrame:
    """
    Возвращает датафрейм транзакций за период. Принимает дату начала и дату конца периода.
    """
    excel_data = get_transactions_from_xlsx_file()
    excel_data['date'] = pd.to_datetime(excel_data['Дата операции'],dayfirst=True)
    filtered_transactions = excel_data.loc[(excel_data['date']>date_from) & (excel_data['date']<date_to) & (excel_data['Сумма операции']<0)]
    return filtered_transactions


def get_user_settings(filepath: str = SETTINGS_PATH) -> DataFrame:
    file_to_open = file(filepath)
    try:
        with open(file_to_open, "r", encoding="utf8") as f:
            data = json.load(f)
            # logger.debug("Файл успешно распарсен.")
            return data
    except Exception as e:
        raise e

if __name__ == '__main__':
   result_dict = get_transactions_from_xlsx_file()
   print(result_dict.head())
   print(get_user_settings())
