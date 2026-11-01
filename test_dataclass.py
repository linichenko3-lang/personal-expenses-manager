from datetime import date

from expense_tracker.dataclass_models import (
    Transaction,
    TransactionType,
)
from expense_tracker.dataclass_models import Budget


income = Transaction(
    amount=5000,
    transaction_type=TransactionType.INCOME,
    category="Salary",
    date=date(2024, 3, 15),
)

expense = Transaction(
    amount=350,
    transaction_type=TransactionType.EXPENSE,
    category="Food",
    date=date(2024, 3, 15),
)

print(income.formatted())
print(expense.formatted())

print("Income is expense:", income.is_expense())
print("Expense is expense:", expense.is_expense())


print("\n===== ТЕСТ BUDGET =====")

budget = Budget(
    category="Food",
    monthly_limit=5000,
    spent=1500,
)

print("Категорія:", budget.category)
print("Місячний ліміт:", budget.monthly_limit)
print("Витрачено:", budget.spent)
print("Залишок:", budget.remaining())
print("Перевищено:", budget.is_exceeded())
print("Використання бюджету:", budget.utilization_pct(), "%")