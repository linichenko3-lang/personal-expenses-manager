from datetime import date
from expense_tracker.database import init_db
from expense_tracker.models import (
    Transaction,
    Income,
    Expense,
    Budget,
    create_user,
    get_user_by_email,
    get_all_transactions,
    get_all_budgets,
    add_transaction as add_transaction_to_db,
    delete_transaction as delete_transaction_from_db,
    set_budget as set_budget_in_db,
    delete_budget as delete_budget_from_db,
)
from expense_tracker.decorators import (
    log_transaction,
    validate_amount,
    currency_aware,
)


from expense_tracker.exceptions import TransactionNotFoundError

class ExpenseTracker:
    """Керує транзакціями та розрахунками особистих фінансів."""

    def __init__(self):
        init_db()

        username = "Expense Tracker User"
        email = "app@example.com"

        user = get_user_by_email(email)

        if user is None:
            self.user_id = create_user(username, email)
        else:
            self.user_id = user["id"]

        self._transactions = self._load_transactions_from_db()
        self._budgets = self._load_budgets_from_db()

    def _load_transactions_from_db(self):
        """Завантажує транзакції з SQLite та створює об'єкти."""

        transactions = get_all_transactions(self.user_id)

        result = []

        for item in transactions:

            if item["transaction_type"] == "income":
                transaction_data = item.copy()
                transaction_data["variable"] = bool(
                    item["variable"]
                )

                transaction = Income.from_dict(transaction_data)

            elif item["transaction_type"] == "expense":
                transaction_data = item.copy()
                transaction_data["is_recurring"] = bool(
                    item["is_recurring"]
                )

                transaction = Expense.from_dict(transaction_data)

            else:
                raise ValueError(
                    f"Невідомий тип транзакції: "
                    f"{item['transaction_type']}"
                )

            transaction._db_id = item["id"]

            result.append(transaction)

        return result
    
    def _load_budgets_from_db(self):
        """Завантажує бюджети з SQLite та створює об'єкти Budget."""

        budgets = get_all_budgets(self.user_id)

        result = []

        for item in budgets:
            budget = Budget.from_dict(item)
            budget._db_id = item["id"]
            result.append(budget)

        return result

    @property
    def transactions(self):
        """Повертає копію списку транзакцій."""
        return self._transactions.copy()

    @property
    def budgets(self):
        """Повертає копію списку бюджетів."""
        return self._budgets.copy()

    def add_budget(self, budget):
        """Додає бюджет до SQLite."""

        if not isinstance(budget, Budget):
            raise TypeError("Можна додавати лише об'єкти Budget.")

        budget_id = set_budget_in_db(
            user_id=self.user_id,
            category=budget.category,
            monthly_limit=budget.monthly_limit,
        )

        budget._db_id = budget_id

        self._budgets.append(budget)


    def add_transaction(self, transaction):
        """Додає транзакцію до SQLite."""

        if isinstance(transaction, Income):
            transaction_type = "income"
            variable = transaction.variable
            is_recurring = False

        elif isinstance(transaction, Expense):
            transaction_type = "expense"
            variable = False
            is_recurring = transaction.is_recurring

        else:
            raise TypeError(
                "Можна додавати лише об'єкти Income або Expense."
            )

        transaction_id = add_transaction_to_db(
            user_id=self.user_id,
            amount=transaction.amount,
            transaction_type=transaction_type,
            category=transaction.category,
            description=transaction.description,
            variable=variable,
            is_recurring=is_recurring,
            transaction_date=transaction.date,
        )

        transaction._db_id = transaction_id

        self._transactions.append(transaction)

    
    @validate_amount
    @log_transaction
    @currency_aware(base_currency="UAH")


    def add_income(
        self,
        amount,
        category,
        description="",
        transaction_date=None,
        variable=False,
    ):
        """Додає дохід користувача."""

        if transaction_date is None:
            transaction_date = date.today().isoformat()

        income = Income(
            amount=amount,
            category=category,
            date=transaction_date,
            description=description,
            variable=variable,
        )

        self.add_transaction(income)

        return income

    @validate_amount
    @log_transaction
    @currency_aware(base_currency="UAH")
    def add_expense(
        self,
        amount,
        category,
        description="",
        transaction_date=None,
        is_recurring=False,
    ):
        """Додає витрату користувача."""

        if transaction_date is None:
            transaction_date = date.today().isoformat()

        expense = Expense(
            amount=amount,
            category=category,
            date=transaction_date,
            description=description,
            is_recurring=is_recurring,
        )

        self.add_transaction(expense)

        return expense

    def delete_budget(self, category):
        """Видаляє бюджет із SQLite та списку об'єктів."""

        for budget in self._budgets:
            if budget.category == category:

                budget_id = getattr(budget, "_db_id", None)

                if budget_id is None:
                    raise ValueError(
                        "Бюджет не має ID у базі даних."
                    )

                deleted = delete_budget_from_db(
                    self.user_id,
                    budget_id,
                )

                if not deleted:
                    raise ValueError(
                        "Бюджет не знайдено в базі даних."
                    )

                self._budgets.remove(budget)
                return

        raise ValueError(
            f"Бюджет для категорії '{category}' не знайдено."
        )



    @log_transaction
    def delete_transaction(self, transaction_id):
        """Видаляє транзакцію з SQLite за її ID."""

        transaction = next(
            (
                item
                for item in self._transactions
                if getattr(item, "_db_id", None) == transaction_id
            ),
            None,
        )

        if transaction is None:
            raise TransactionNotFoundError(
                "Такої транзакції немає."
            )

        deleted = delete_transaction_from_db(transaction_id)

        if not deleted:
            raise TransactionNotFoundError(
                "Транзакцію не знайдено в базі даних."
            )

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
