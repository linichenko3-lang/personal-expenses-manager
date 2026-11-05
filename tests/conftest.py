import pytest
from datetime import date

from expense_tracker.dataclass_models import (
    Transaction,
    TransactionType,
    Budget,
)


@pytest.fixture
def expense_transaction():
    """Тестова транзакція — витрата."""
    return Transaction(
        amount=100,
        transaction_type=TransactionType.EXPENSE,
        category="Їжа",
        date=date(2026, 11, 5),
    )


@pytest.fixture
def income_transaction():
    """Тестова транзакція — дохід."""
    return Transaction(
        amount=5000,
        transaction_type=TransactionType.INCOME,
        category="Зарплата",
        date=date(2026, 11, 5),
    )


@pytest.fixture
def budget():
    """Тестовий бюджет."""
    return Budget(
        category="Їжа",
        monthly_limit=1000,
        spent=400,
    )
