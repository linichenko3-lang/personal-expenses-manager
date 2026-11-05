from datetime import date
import math

from expense_tracker.dataclass_models import (
    Transaction,
    TransactionType,
    Budget,
)


# ===== TRANSACTION =====

def test_transaction_is_expense(expense_transaction):
    assert expense_transaction.is_expense() is True


def test_transaction_is_income(income_transaction):
    assert income_transaction.is_expense() is False


def test_transaction_formatted(expense_transaction):
    assert expense_transaction.formatted() == (
        "- 100.00 UAH [Їжа] 2026-11-05"
    )


def test_income_formatted(income_transaction):
    assert income_transaction.formatted() == (
        "+ 5000.00 UAH [Зарплата] 2026-11-05"
    )


def test_transaction_default_date():
    transaction = Transaction(
        amount=100,
        transaction_type=TransactionType.EXPENSE,
        category="Їжа",
    )

    assert transaction.date == date.today()


def test_transaction_empty_description():
    transaction = Transaction(
        amount=100,
        transaction_type=TransactionType.EXPENSE,
        category="Їжа",
    )

    assert transaction.description == ""


# ===== BUDGET =====

def test_budget_remaining(budget):
    assert budget.remaining() == 600


def test_budget_not_exceeded(budget):
    assert budget.is_exceeded() is False


def test_budget_exceeded():
    budget = Budget(
        category="Їжа",
        monthly_limit=1000,
        spent=1200,
    )

    assert budget.is_exceeded() is True


def test_budget_remaining_at_exact_limit():
    budget = Budget(
        category="Їжа",
        monthly_limit=1000,
        spent=1000,
    )

    assert budget.remaining() == 0


def test_budget_not_exceeded_at_exact_limit():
    budget = Budget(
        category="Їжа",
        monthly_limit=1000,
        spent=1000,
    )

    assert budget.is_exceeded() is False


def test_budget_utilization_at_exact_limit():
    budget = Budget(
        category="Їжа",
        monthly_limit=1000,
        spent=1000,
    )

    assert budget.utilization_pct() == 100.0


def test_budget_utilization_pct(budget):
    assert budget.utilization_pct() == 40.0


def test_budget_zero_limit():
    budget = Budget(
        category="Їжа",
        monthly_limit=0,
        spent=0,
    )

    assert budget.utilization_pct() == 0.0


def test_budget_infinite_utilization():
    budget = Budget(
        category="Їжа",
        monthly_limit=0,
        spent=100,
    )

    assert math.isinf(budget.utilization_pct())