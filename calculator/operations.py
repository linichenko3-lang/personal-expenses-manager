def add(a: float, b: float) -> float:
        """Повертає суму двох чисел.

    Args:
        a: Перше число.
        b: Друге число.

    Returns:
        Сума a та b.

    Example:
        >>> add(3, 5)
        8.0"""
        return a + b

def subtract(a: float, b: float) -> float:
    """Повертає різницю двох чисел (a мінус b).

    Args:
        a: Від'ємне число (зменшуване).
        b: Число, яке віднімається (від'ємник).

    Returns:
        Різниця a та b.

    Example:
        >>> subtract(10, 3)
        7.0
    """
    return a - b

def multiply(a: float, b: float) -> float:
    """Повертає добуток двох чисел.

    Args:
        a: Перший множник.
        b: Другий множник.

    Returns:
        Добуток a та b.

    Example:
        >>> multiply(4, 3)
        12.0
    """
    return a * b

def divide(a: float, b: float) -> float:
    """Ділить a на b і повертає результат.

    Args:
        a: Ділене.
        b: Дільник. Не може бути нулем.

    Returns:
        Частка a та b.

    Raises:
        ValueError: Якщо b дорівнює нулю.

    Example:
        >>> divide(10, 2)
        5.0
    """
    if b == 0:
        raise ValueError("Ділення на нуль неможливе. Введіть ненульовий дільник.")
    return a / b