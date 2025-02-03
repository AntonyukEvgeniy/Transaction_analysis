import functools
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar

import pandas as pd

F = TypeVar("F", bound=Callable[..., Any])


def log_result_to_file(*, filename: str) -> Callable[[F], F]:
    """
    Декоратор для записи результата выполнения функции в файл.

    Args:
        filename (str): Путь к файлу для записи результата

    Returns:
        Callable: Декорированная функция
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            if not filename:
                print(result)
                return result

            file_path = Path(__file__).parent.parent / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result.to_string() if isinstance(result, pd.DataFrame) else str(result))
            return result

        return wrapper  # type: ignore

    return decorator


def log(file: str = "") -> Callable[[Callable], Callable]:
    """
    Декоратор для логирования выполнения функции.

    Args:
        file (str): Путь к файлу для записи логов. Если пустой - вывод в консоль

    Returns:
        Callable: Декорированная функция, которая логирует свое выполнение
    """

    def logger(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            file_path = Path(__file__).parent.parent / file if file else None
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
            except Exception as e:
                log_message = f"{func.__name__} error: {repr(e)}. Inputs: {args}, {kwargs}"
                result = None

            if file_path:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(f"\n{log_message}")
            else:
                print(log_message)
            return result

        return wrapped

    return logger
