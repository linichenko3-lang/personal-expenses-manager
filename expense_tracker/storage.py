import json
from pathlib import Path

from expense_tracker.models import Income, Expense, Budget


# Шлях до папки data у корені проєкту
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TRANSACTIONS_FILE = DATA_DIR / "transactions.json"
BUDGETS_FILE = DATA_DIR / "budgets.json"


def save_transactions(transactions):
    """Зберігає список транзакцій у JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = [transaction.to_dict() for transaction in transactions]

    with TRANSACTIONS_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_transactions():
    """Завантажує транзакції з JSON."""
    if not TRANSACTIONS_FILE.exists():
        return []

    with TRANSACTIONS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    transactions = []

    for item in data:
        if item["type"] == "income":
            transactions.append(Income.from_dict(item))
        elif item["type"] == "expense":
            transactions.append(Expense.from_dict(item))
        else:
            raise ValueError(
                f"Невідомий тип транзакції: {item['type']}"
            )

    return transactions


def save_budgets(budgets):
    """Зберігає список бюджетів у JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = [budget.to_dict() for budget in budgets]

    with BUDGETS_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_budgets():
    """Завантажує бюджети з JSON."""
    if not BUDGETS_FILE.exists():
        return []

    with BUDGETS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [Budget.from_dict(item) for item in data]
