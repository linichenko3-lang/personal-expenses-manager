from expense_tracker.storage import (
    load_transactions,
    save_transactions,
    load_budgets,
    save_budgets,
)

from datetime import date

from expense_tracker.models import Transaction, Income, Expense, Budget

from expense_tracker.exceptions import TransactionNotFoundError

class ExpenseTracker:
    """Керує транзакціями та розрахунками особистих фінансів."""

    def __init__(self):
        self._transactions = load_transactions()
        self._budgets = load_budgets()

    @property
    def transactions(self):
        """Повертає копію списку транзакцій."""
        return self._transactions.copy()

    @property
    def budgets(self):
        """Повертає копію списку бюджетів."""
        return self._budgets.copy()

    def add_budget(self, budget):
        """Додає бюджет і зберігає його у JSON."""
        if not isinstance(budget, Budget):
            raise TypeError("Можна додавати лише об'єкти Budget.")

        self._budgets.append(budget)
        save_budgets(self._budgets)


    def add_transaction(self, transaction):
        """Додає транзакцію до списку."""
        if not isinstance(transaction, Transaction):
            raise TypeError(
                "Можна додавати лише об'єкти Transaction, Income або Expense."
            )
        
        self._transactions.append(transaction)
        save_transactions(self._transactions)


    def delete_budget(self, category):
        """Видаляє бюджет за категорією та зберігає зміни."""
        for budget in self._budgets:
            if budget.category == category:
                self._budgets.remove(budget)
                save_budgets(self._budgets)
                return

        raise ValueError(
            f"Бюджет для категорії '{category}' не знайдено."
        )



    def delete_transaction(self, transaction):
        """Видаляє конкретну транзакцію."""
        if transaction not in self._transactions:
            raise TransactionNotFoundError(
                "Такої транзакції немає у списку."
            )

        self._transactions.remove(transaction)
        self._transactions.remove(transaction)

    def calculate_balance(self):
        """Обчислює загальний баланс усіх транзакцій."""
        return sum(
            transaction.calculate_balance
            for transaction in self._transactions
        )

    def monthly_report(self, year, month):
        """Повертає звіт про доходи та витрати за вказаний місяць."""
        if isinstance(year, bool) or not isinstance(year, int):
            raise TypeError("Рік має бути цілим числом.")

        if isinstance(month, bool) or not isinstance(month, int):
            raise TypeError("Місяць має бути цілим числом.")

        if not 1 <= month <= 12:
            raise ValueError("Місяць має бути від 1 до 12.")

        if not 1 <= year <= 9999:
            raise ValueError("Некоректний рік.")

        monthly_transactions = [
            transaction
            for transaction in self._transactions
            if date.fromisoformat(transaction.date).year == year
            and date.fromisoformat(transaction.date).month == month
        ]

        total_income = sum(
            transaction.amount
            for transaction in monthly_transactions
            if isinstance(transaction, Income)
        )

        total_expenses = sum(
            transaction.amount
            for transaction in monthly_transactions
            if isinstance(transaction, Expense)
        )

        return {
            "year": year,
            "month": month,
            "income": total_income,
            "expenses": total_expenses,
            "balance": total_income - total_expenses,
            "transactions": monthly_transactions,
        }
