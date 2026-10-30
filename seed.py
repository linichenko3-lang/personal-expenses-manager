from expense_tracker.models import (
    create_user,
    add_transaction,
    get_all_transactions,
    get_balance,
    get_expenses_by_category,
    set_budget,
)
from expense_tracker.models import check_budget_status


user_id = create_user("Demo User", "demo@example.com")

print(f"Створено користувача. ID: {user_id}")

# Доходи
add_transaction(
    user_id, 15000, "income", "Salary", "Monthly salary"
)

add_transaction(
    user_id, 2000, "income", "Bonus", "Project bonus"
)

# Витрати
add_transaction(
    user_id, 450, "expense", "Food", "Groceries"
)

add_transaction(
    user_id, 120, "expense", "Transport", "Bus ticket"
)

add_transaction(
    user_id, 300, "expense", "Food", "Market"
)

add_transaction(
    user_id, 80, "expense", "Transport", "Metro"
)

add_transaction(
    user_id, 200, "expense", "Health", "Pharmacy"
)

set_budget(user_id, "Food", 5000)
set_budget(user_id, "Transport", 1500)

print("\n=== Транзакції ===")

transactions = get_all_transactions(user_id)

for transaction in transactions:
    amount = transaction["amount"]

    if transaction["transaction_type"] == "expense":
        amount = -amount

    print(
        f"[{transaction['id']}] "
        f"{transaction['date']} | "
        f"{transaction['transaction_type']:<7} | "
        f"{transaction['category']:<10} | "
        f"{amount:+.2f}"
    )

print(f"\n=== Баланс: {get_balance(user_id):.2f} ===")

print("\n=== Витрати за категоріями ===")

expenses = get_expenses_by_category(user_id)

for expense in expenses:
    print(
        f"{expense['category']:<12}: "
        f"{expense['total_expenses']:.2f}"
    )

print("\n=== СТАН БЮДЖЕТІВ ===")

budget_statuses = check_budget_status(user_id)

for status in budget_statuses:
    print(
        f"{status['category']}: "
        f"{status['total_expenses']:.2f} / "
        f"{status['monthly_limit']:.2f} грн"
    )

    if status["exceeded"]:
        print(
            f"УВАГА! Перевищено бюджет "
            f"категорії {status['category']}!"
        )

