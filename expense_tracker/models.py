from abc import ABC, abstractmethod
from datetime import date
from expense_tracker.exceptions import InvalidAmountError
from expense_tracker.constants import IncomeCategory, ExpenseCategory

class Transaction(ABC):
    """Абстрактний базовий клас для доходів і витрат."""

    def __init__(self, amount, category, date, description):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidAmountError("Сума має бути числом.")

        if value <= 0:
            raise InvalidAmountError("Сума має бути більшою за нуль.")

        self._amount = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Категорія не може бути порожньою.")
        self._category = value.strip()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, str):
            raise TypeError("Дата має бути рядком YYYY-MM-DD.")
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError("Некоректна дата. Використай YYYY-MM-DD.")
        self._date = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Опис має бути рядком.")
        self._description = value.strip()

    @property
    @abstractmethod
    def calculate_balance(self):
        """Повертає суму зі знаком відповідно до типу транзакції."""
        pass

    def display_transaction(self):
        print(f"Сума: {self.amount} грн")
        print(f"Категорія: {self.category}")
        print(f"Дата: {self.date}")
        print(f"Опис: {self.description}")


class Income(Transaction):
    """Клас для доходів."""

    def __init__(self, amount, category, date, description, variable):
        super().__init__(amount, category, date, description)
        self.variable = variable

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, IncomeCategory):
            value = value.value

        if not isinstance(value, str):
            raise TypeError("Категорія доходу має бути рядком.")

        if value not in [category.value for category in IncomeCategory]:
            raise ValueError(f"Недопустима категорія доходу: {value}")

        self._category = value

    @property
    def variable(self):
        return self._variable

    @variable.setter
    def variable(self, value):
        if not isinstance(value, bool):
            raise TypeError("variable має бути True або False.")
        self._variable = value

    @property
    def calculate_balance(self):
        return self.amount

    def display_transaction(self):
        super().display_transaction()
        print(f"Змінний дохід: {self.variable}")


class Expense(Transaction):
    """Клас для витрат."""

    def __init__(self, amount, category, date, description, is_recurring):
        super().__init__(amount, category, date, description)
        self.is_recurring = is_recurring

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, ExpenseCategory):
            value = value.value

        if not isinstance(value, str):
            raise TypeError("Категорія витрати має бути рядком.")

        if value not in [category.value for category in ExpenseCategory]:
            raise ValueError(f"Недопустима категорія витрати: {value}")

        self._category = value

    @property
    def is_recurring(self):
        return self._is_recurring

    @is_recurring.setter
    def is_recurring(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_recurring має бути True або False.")
        self._is_recurring = value

    @property
    def calculate_balance(self):
        return -self.amount

    def display_transaction(self):
        super().display_transaction()
        print(f"Регулярна витрата: {self.is_recurring}")


class Budget:
    """Бюджет з установленим місячним лімітом."""

    def __init__(self, category, monthly_limit):
        self.category = category
        self.monthly_limit = monthly_limit

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Категорія не може бути порожньою.")
        self._category = value.strip()

    @property
    def monthly_limit(self):
        return self._monthly_limit

    @monthly_limit.setter
    def monthly_limit(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Місячний ліміт має бути числом.")
        if value < 0:
            raise ValueError("Місячний ліміт не може бути від'ємним.")
        self._monthly_limit = value

    def display_budget(self):
        print(f"Категорія: {self.category}")
        print(f"Місячний ліміт: {self.monthly_limit} грн")

    def calculate_total_expenses(self, transactions):
        return sum(
            transaction.amount
            for transaction in transactions
            if isinstance(transaction, Expense)
            and transaction.category == self.category
        )

    def check_budget(self, transactions):
        total_expenses = self.calculate_total_expenses(transactions)

        if total_expenses > self.monthly_limit:
            over_limit = total_expenses - self.monthly_limit
            print(f"Перевищено ліміт для категорії {self.category}!")
            print(f"Сума витрат: {total_expenses} грн")
            print(f"Перевищення: {over_limit} грн")
        else:
            remaining = self.monthly_limit - total_expenses
            print(f"Витрати в межах бюджету для категорії {self.category}.")
            print(f"Залишок бюджету: {remaining} грн")

    def monthly_report(self, transactions):
        total_expenses = self.calculate_total_expenses(transactions)
        remaining = self.monthly_limit - total_expenses

        print(f"Звіт по категорії {self.category}:")
        print(f"Місячний ліміт: {self.monthly_limit} грн")
        print(f"Витрати за місяць: {total_expenses} грн")

        if remaining < 0:
            print(f"Перевищення бюджету: {-remaining} грн")
        else:
            print(f"Залишок бюджету: {remaining} грн")
