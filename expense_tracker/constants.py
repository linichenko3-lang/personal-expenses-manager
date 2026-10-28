from enum import Enum


class IncomeCategory(str, Enum):
    """Категорії доходів."""

    SALARY = "Зарплата"
    BONUS = "Премія"
    FREELANCE = "Фриланс"
    INVESTMENTS = "Інвестиції"
    OTHER = "Інше"


class ExpenseCategory(str, Enum):
    """Категорії витрат."""

    FOOD = "Їжа"
    RENT = "Оренда"
    UTILITIES = "Комунальні послуги"
    TRANSPORT = "Транспорт"
    HEALTH = "Здоров'я"
    ENTERTAINMENT = "Розваги"
    EDUCATION = "Освіта"
    CLOTHING = "Одяг"
    OTHER = "Інше"
