# main.py
"""
Арифметичний калькулятор — точка входу програми.

Запуск:
    uv run main.py
    або
    python main.py
"""
from calculator.operations import add, subtract, multiply, divide

# Словник операцій: символ → функція
OPERATIONS: dict[str, callable] = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

def get_number(prompt: str) -> float:
    """Запитує у користувача число, повторює при невалідному введенні.

    Args:
        prompt: Текст запиту для користувача.

    Returns:
        Число типу float, введене користувачем.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            return float(user_input)
        except ValueError:
            print(f"  Помилка: '{user_input}' — не є числом. Спробуйте ще раз.\n")

def get_operation() -> str:

    """ Запитує у користувача операцію, повторює при невалідному введенні.

    Returns:
        Рядок з символом операції (+, -, *, /) або 'q' для виходу.
    """
    available = list(OPERATIONS.keys())
    while True:
        user_input = input(f"Оберіть операцію {available} або 'q' для виходу: ").strip()
        if user_input == "q":
            return "q"
        if user_input in OPERATIONS:
            return user_input
        print(f"  Помилка: операція '{user_input}' не підтримується.\n")
def calculate(a: float, op: str, b: float) -> float | None:
    """Виконує обрану операцію над двома числами.

    Args:
        a: Перше число.
        op: Символ операції.
        b: Друге число.

    Returns:
        Результат обчислення або None у разі помилки.
    """
    try:
        result = OPERATIONS[op](a, b)
        return result
    except ValueError as error:
        print(f"  Помилка: {error}\n")
        return None

def format_result(a: float, op: str, b: float, result: float) -> str:
    """Форматує рядок результату, видаляючи зайві нулі у цілих чисел.

    Args:
        a: Перше число.
        op: Символ операції.
        b: Друге число.
        result: Результат обчислення.

    Returns:
        Відформатований рядок із результатом.
    """
    # Виводимо ціле число без .0, якщо результат цілий
    def fmt(n: float) -> str:
        return str(int(n)) if n == int(n) else str(n)

    return f"  {fmt(a)} {op} {fmt(b)} = {fmt(result)}"

def main() -> None:
    """Головна функція — запускає інтерактивний цикл калькулятора."""
    print("=" * 40)
    print("  Арифметичний калькулятор")
    print("=" * 40)
    print("Підтримувані операції: +, -, *, /")
    print("Введіть 'q' для виходу.\n")

    while True:
        op = get_operation()

        if op == "q":
            print("\nДо побачення!")
            break

        a = get_number("Введіть перше число:  ")
        b = get_number("Введіть друге число:  ")

        result = calculate(a, op, b)

        if result is not None:
            print("\nРезультат:")
            print(format_result(a, op, b, result))
            print()


if __name__ == "__main__":
    main()
    