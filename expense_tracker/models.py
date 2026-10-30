from abc import ABC, abstractmethod
from datetime import date
from expense_tracker.exceptions import InvalidAmountError
from expense_tracker.constants import IncomeCategory, ExpenseCategory
from expense_tracker.database import get_connection


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


    def to_dict(self):
        """Перетворює об'єкт Income на словник."""
        return {
            "type": "income",
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
            "variable": self.variable,
        }

    @classmethod
    def from_dict(cls, data):
        """Створює об'єкт Income зі словника."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            description=data["description"],
            variable=data["variable"],
        )



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


    def to_dict(self):
        """Перетворює об'єкт Expense на словник."""
        return {
            "type": "expense",
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
            "is_recurring": self.is_recurring,
        }

    @classmethod
    def from_dict(cls, data):
        """Створює об'єкт Expense зі словника."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            description=data["description"],
            is_recurring=data["is_recurring"],
        )



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


    def to_dict(self):
        """Перетворює об'єкт Budget на словник."""
        return {
            "category": self.category,
            "monthly_limit": self.monthly_limit,
        }

    @classmethod
    def from_dict(cls, data):
        """Створює об'єкт Budget зі словника."""
        return cls(
            category=data["category"],
            monthly_limit=data["monthly_limit"],
        )

def create_user(username, email):
    """Створює користувача та повертає його ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (username, email)
            VALUES (?, ?)
            """,
            (username, email),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()

def get_user_by_email(email):
    """Знаходить користувача за електронною адресою."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, username, email
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        user = cursor.fetchone()

        return dict(user) if user else None

    finally:
        connection.close()

def add_transaction(
    user_id,
    amount,
    transaction_type,
    category,
    description,
    variable=False,
    is_recurring=False,
    transaction_date=None,
):
    """Додає транзакцію користувача та повертає її ID."""

    if amount <= 0:
        raise ValueError("Сума транзакції має бути більшою за нуль.")

    if transaction_type not in ("income", "expense"):
        raise ValueError(
            "Тип транзакції повинен бути 'income' або 'expense'."
        )

    if transaction_date is None:
        transaction_date = date.today().isoformat()
    else:
        try:
            date.fromisoformat(transaction_date)
        except (ValueError, TypeError):
            raise ValueError("Некоректна дата. Використай YYYY-MM-DD.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO transactions (
                amount,
                transaction_type,
                category,
                date,
                description,
                variable,
                is_recurring,
                user_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                amount,
                transaction_type,
                category,
                transaction_date,
                description,
                int(variable),
                int(is_recurring),
                user_id,
            ),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()

def get_all_transactions(user_id):
    """Повертає всі транзакції конкретного користувача."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                amount,
                transaction_type,
                category,
                date,
                description,
                variable,
                is_recurring
            FROM transactions
            WHERE user_id = ?
            ORDER BY date, id
            """,
            (user_id,),
        )

        transactions = cursor.fetchall()

        return [dict(transaction) for transaction in transactions]

    finally:
        connection.close()

def get_balance(user_id):
    """Обчислює баланс конкретного користувача."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'income' THEN amount
                            WHEN transaction_type = 'expense' THEN -amount
                        END
                    ),
                    0
                ) AS balance
            FROM transactions
            WHERE user_id = ?
            """,
            (user_id,),
        )

        result = cursor.fetchone()

        return float(result["balance"])

    finally:
        connection.close()

def get_expenses_by_category(user_id):
    """Повертає загальні витрати користувача за категоріями."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                category,
                SUM(amount) AS total_expenses
            FROM transactions
            WHERE user_id = ?
                AND transaction_type = 'expense'
            GROUP BY category
            ORDER BY category
            """,
            (user_id,),
        )

        expenses = cursor.fetchall()

        return [dict(expense) for expense in expenses]

    finally:
        connection.close()

def set_budget(user_id, category, monthly_limit):
    """Створює бюджет користувача та повертає його ID."""

    if monthly_limit <= 0:
        raise ValueError("Місячний ліміт має бути більшим за нуль.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO budgets (
                category,
                monthly_limit,
                user_id
            )
            VALUES (?, ?, ?)
            """,
            (category, monthly_limit, user_id),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()

def delete_budget(user_id, budget_id):
    """Видаляє бюджет користувача за ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM budgets
            WHERE id = ? AND user_id = ?
            """,
            (budget_id, user_id),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()

def get_all_budgets(user_id):
    """Повертає всі бюджети конкретного користувача."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                category,
                monthly_limit
            FROM budgets
            WHERE user_id = ?
            ORDER BY category
            """,
            (user_id,),
        )

        budgets = cursor.fetchall()

        return [dict(budget) for budget in budgets]

    finally:
        connection.close()


def delete_transaction(transaction_id):
    """Видаляє транзакцію за ID та повертає результат."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM transactions
            WHERE id = ?
            """,
            (transaction_id,),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()

def check_budget_status(user_id):
    """Перевіряє витрати користувача відносно місячних бюджетів."""

    current_month = date.today().strftime("%Y-%m")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                budgets.category,
                budgets.monthly_limit,
                COALESCE(SUM(transactions.amount), 0) AS total_expenses
            FROM budgets

            LEFT JOIN transactions
                ON budgets.user_id = transactions.user_id
                AND budgets.category = transactions.category
                AND transactions.transaction_type = 'expense'
                AND strftime('%Y-%m', transactions.date) = ?

            WHERE budgets.user_id = ?

            GROUP BY
                budgets.id,
                budgets.category,
                budgets.monthly_limit

            ORDER BY budgets.category
            """,
            (current_month, user_id),
        )

        rows = cursor.fetchall()

        result = []

        for row in rows:
            total_expenses = float(row["total_expenses"])
            monthly_limit = float(row["monthly_limit"])

            result.append({
                "category": row["category"],
                "monthly_limit": monthly_limit,
                "total_expenses": total_expenses,
                "exceeded": total_expenses > monthly_limit,
            })

        return result

    finally:
        connection.close()