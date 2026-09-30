# calculator/__init__.py
"""
Пакет calculator — арифметичні операції.

Надає чотири базові математичні функції:
    - add(a, b)       → a + b
    - subtract(a, b)  → a − b
    - multiply(a, b)  → a × b
    - divide(a, b)    → a ÷ b (з обробкою ділення на нуль)
"""
from calculator.operations import add, subtract, multiply, divide
__all__ = ["add", "subtract", "multiply", "divide"]
