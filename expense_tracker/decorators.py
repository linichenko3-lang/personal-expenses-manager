import logging
import functools
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(
            "expense_tracker.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

def log_transaction(func):
    """
    Логує фінансові операції:
    тип операції, суму, категорію та час.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Фіксуємо час виклику
        operation_time = datetime.now()

        # Викликаємо початкову функцію
        result = func(*args, **kwargs)

        # Отримуємо назву методу
        function_name = func.__name__

        if function_name == "delete_transaction":
            transaction_id = kwargs.get(
                "transaction_id",
                args[1] if len(args) > 1 else None
            )

            logging.info(
                "%s: id=%s, час=%s",
                function_name,
                transaction_id,
                operation_time.strftime("%H:%M:%S")
            )

        else:
            amount = kwargs.get(
                "amount",
                args[1] if len(args) > 1 else None
            )

            category = kwargs.get(
                "category",
                args[2] if len(args) > 2 else None
            )

            logging.info(
                "%s: сума=%s, категорія='%s', час=%s",
                function_name,
                amount,
                category,
                operation_time.strftime("%H:%M:%S")
            )

        return result

    return wrapper

def validate_amount(func):
    """
    Перевіряє, що сума є числом і більшою за нуль.
    Якщо перевірка не пройдена, повертає None.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Отримуємо значення amount
        if "amount" in kwargs:
            amount = kwargs["amount"]

        elif len(args) > 1:
            # Для методу класу: args[0] — self
            amount = args[1]

        elif len(args) == 1:
            # Для звичайної функції
            amount = args[0]

        else:
            amount = None

        # Перевіряємо тип і значення суми
        if (
            isinstance(amount, bool)
            or not isinstance(amount, (int, float))
            or amount <= 0
        ):
            logging.warning(
                "validate_amount: сума має бути > 0, отримано: %s",
                amount,
            )
            return None

        return func(*args, **kwargs)

    return wrapper

def currency_aware(base_currency="UAH"):
    """
    Заглушка для майбутньої конвертації валют.
    Конвертація буде реалізована пізніше.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            logging.debug(
                f"[currency_aware] Конвертація ще не реалізована. "
                f"Базова валюта: {base_currency}"
            )

            return func(*args, **kwargs)

        return wrapper

    return decorator
