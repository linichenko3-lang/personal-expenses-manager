from datetime import date
from functools import reduce

from expense_tracker.dataclass_models import (
    Transaction,
    TransactionType,
)

transactions: list[Transaction] = [
    # Доходи
    Transaction(
        15000, TransactionType.INCOME,
        "Salary", date(2024, 3, 15), "Monthly salary"
    ),
    Transaction(
        2000, TransactionType.INCOME,
        "Bonus", date(2024, 3, 16), "Project bonus"
    ),
    Transaction(
        3500, TransactionType.INCOME,
        "Freelance", date(2024, 3, 18), "Freelance work"
    ),

    # Витрати
    Transaction(
        450, TransactionType.EXPENSE,
        "food", date(2024, 3, 19), "Groceries"
    ),
    Transaction(
        120, TransactionType.EXPENSE,
        "transport", date(2024, 3, 20), "Bus ticket"
    ),
    Transaction(
        300, TransactionType.EXPENSE,
        "food", date(2024, 3, 21), "Market"
    ),
    Transaction(
        200, TransactionType.EXPENSE,
        "health", date(2024, 3, 22), "Pharmacy"
    ),
    Transaction(
        500, TransactionType.EXPENSE,
        "entertainment", date(2024, 3, 23), "Cinema"
    ),
    Transaction(
        80, TransactionType.EXPENSE,
        "transport", date(2024, 3, 24), "Metro"
    ),
]

expenses = list(
    filter(lambda t: t.is_expense(), transactions)
)

incomes = list(
    filter(lambda t: not t.is_expense(), transactions)
)

# Загальна сума витрат
total_expenses = reduce(
    lambda acc, amount: acc + amount,
    map(lambda t: t.amount, expenses),
    0.0,
)

# Загальна сума доходів
total_incomes = reduce(
    lambda acc, amount: acc + amount,
    map(lambda t: t.amount, incomes),
    0.0,
)

food_expenses = list(
    map(
        lambda t: t.formatted(),
        filter(
            lambda t: t.category.lower() == "food",
            expenses,
        ),
    )
)
sorted_by_amount = sorted(
    transactions,
    key=lambda t: t.amount,
    reverse=True,
)

print("\n=== Всі транзакції ===")

for transaction in sorted_by_amount:
    print(transaction.formatted())


print("\n=== Витрати Food ===")

for transaction in food_expenses:
    print(transaction)


print("\n=== Фінансовий звіт ===")

balance = total_incomes - total_expenses

print(f"Доходи:  +{total_incomes:.2f} UAH")
print(f"Витрати: -{total_expenses:.2f} UAH")
print(f"Баланс:   {balance:.2f} UAH")
