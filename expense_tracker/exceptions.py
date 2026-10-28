class ExpenseTrackerError(Exception):
    """Базовий виняток проєкту Expense Tracker."""
    pass


class InvalidAmountError(ExpenseTrackerError):
    """Некоректна сума доходу або витрати."""
    pass


class TransactionNotFoundError(ExpenseTrackerError):
    """Транзакцію не знайдено."""
    pass


class BudgetExceededError(ExpenseTrackerError):
    """Перевищено встановлений бюджет."""
    pass
