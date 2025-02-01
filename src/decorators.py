import functools
from functools import wraps
from pathlib import Path
from typing import Callable, Any

import pandas as pd


def log_result_to_file(*, filename: str):
    """
    Декоратор записывает результат работы функции в файл .txt
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            data_folder = Path(__file__).parent.parent
            file_to_open = data_folder / filename
            if filename != "":
                with open(file_to_open, "w", encoding="utf-8") as f:
                    f.write(result.to_string() if isinstance(result, pd.DataFrame) else str(result))
                return result
            else:
                print(f"{result}")
                return result

        return wrapper

    return decorator


def log(file: str = "") -> Any:
    """
    Декоратор, который логирует выполнение функции в файл либо в консоль, в зависимости от параметра file
    Ожидаемый вывод в лог-файл mylog.txt
    при успешном выполнении:
    my_function ok
    Ожидаемый вывод при ошибке:
    my_function error: тип ошибки. Inputs: (1, 2), {}
    """

    def logger(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            data_folder = Path(__file__).parent.parent
            file_to_open = data_folder / file
            try:
                func(*args, **kwargs)
                if file != "":
                    f = open(file_to_open, "a")
                    f.write(f"\n{func.__name__} ok")
                else:
                    print(f"{func.__name__} ok")
            except Exception as e:
                if file != "":
                    f = open(file_to_open, "a")
                    f.write(f"\n{func.__name__} error: {repr(e)}. Inputs: {args}, {kwargs}")
                else:
                    print(f"{func.__name__} error: {repr(e)}. Inputs: {args}, {kwargs}")
            return func(*args, **kwargs)

        return wrapped

    return logger
