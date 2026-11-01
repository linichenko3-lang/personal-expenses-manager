from dataclasses import dataclass, field
from datetime import date
from enum import Enum

class TransactionType(Enum):
    """Тип фінансової транзакції."""

    INCOME = "income"
    EXPENSE = "expense"

@dataclass
class Transaction:
    amount: float
    transaction_type: TransactionType
    category: str
    date: date = field(default_factory=date.today)
    description: str = ""

    def is_expense(self) -> bool:
        """Перевіряє, чи є транзакція витратою."""
        return self.transaction_type == TransactionType.EXPENSE

    def formatted(self) -> str:
        """Повертає транзакцію у форматованому вигляді."""

        if self.is_expense():
            sign = "-"
        else:
            sign = "+"

        return (
            f"{sign} {self.amount:.2f} UAH "
            f"[{self.category}] {self.date.isoformat()}"
        )

@dataclass
class Budget:
    category: str
    monthly_limit: float
    spent: float = 0.0

    def remaining(self) -> float:
        """Повертає залишок бюджету."""
        return self.monthly_limit - self.spent

    def is_exceeded(self) -> bool:
        """Перевіряє, чи перевищено бюджет."""
        return self.spent > self.monthly_limit

    def utilization_pct(self) -> float:
        """Повертає відсоток використання бюджету."""
        if self.monthly_limit == 0:
            return 0.0 if self.spent == 0 else float("inf")

        return (self.spent / self.monthly_limit) * 100