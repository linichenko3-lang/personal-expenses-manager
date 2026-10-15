#Expense Tracker

from abc import ABC, abstractmethod

class Transaction(ABC):
    def __init__(self, amount, category, date, description):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    @abstractmethod
    def calculate_balance(self):
        pass

    @abstractmethod
    def display_transaction(self):
        pass

class Income(Transaction):
    def __init__(self, amount, category, date, description, variable):
        super().__init__(amount, category, date, description)
        self.variable = variable

    @property
    def calculate_balance(self):
        return self.amount

    def display_transaction(self):
        super().display_transaction()
        print(f"Змінна: {self.variable}")


    def display_transaction(self):
        super().display_transaction()
        print(f"Змінна: {self.variable}")

class Expense(Transaction):
    def __init__(self, amount, category, date, description, is_recurring):
        super().__init__(amount, category, date, description)
        self.is_recurring = is_recurring

    @property
    def calculate_balance(self):
        return -self.amount

    def display_transaction(self):
        super().display_transaction()
        print(f"Регулярна витрата: {self.is_recurring}")



class Budget:
    def __init__(self, category, monthly_limit):
        self.category = category
        self.monthly_limit = monthly_limit

    def display_budget(self):
        print(f"Категорія: {self.category}")
        print(f"Місячний ліміт: {self.monthly_limit} грн")

    def calculate_total_expenses(self, transactions):
        return sum(
            transaction.amount
            for transaction in transactions
            if isinstance(transaction, Expense)
            and transaction.category == self.category
        )

    def check_budget(self, transactions):
        total_expenses = self.calculate_total_expenses(transactions)

        if total_expenses > self.monthly_limit:
            over_limit = total_expenses - self.monthly_limit
            print(f"Перевищено ліміт для категорії {self.category}!")
            print(f"Сума витрат: {total_expenses} грн")
            print(f"Перевищення: {over_limit} грн")
        else:
            remaining = self.monthly_limit - total_expenses
            print(f"Витрати в межах бюджету для категорії {self.category}.")
            print(f"Залишок бюджету: {remaining} грн")

    def monthly_report(self, transactions):
        total_expenses = self.calculate_total_expenses(transactions)
        remaining = self.monthly_limit - total_expenses

        print(f"Звіт по категорії {self.category}:")
        print(f"Місячний ліміт: {self.monthly_limit} грн")
        print(f"Витрати за місяць: {total_expenses} грн")

        if remaining < 0:
            print(f"Перевищення бюджету: {-remaining} грн")
        else:
            print(f"Залишок бюджету: {remaining} грн")


income = Income(
    10000,
    "Зарплата",
    "2026-10-15",
    "Премія",
    True
)
expense = Expense(2000, "Продукти", "2026-10-15", "Покупки", False)

print(income.calculate_balance)   # 10000
print(expense.calculate_balance)  # -2000

income.display_transaction()
expense.display_transaction()

print("---")

expense2 = Expense(3000, "Розваги", "2023-06-03", "Кінотеатр", True)


print("---")

income.display_transaction()

print(f"Баланс доходу: {income.calculate_balance}")
print(f"Баланс витрат: {expense.calculate_balance}")

budgets = [
    Budget("Продукти", 2000),
    Budget("Розваги", 1500),
    Budget("Транспорт", 1000),
]


transactions = [
    Expense(8000, "Продукти", "2023-06-02", "Молочні продукти", True),
    Expense(500, "Розваги", "2023-06-03", "Кіно", True),
    Expense(300, "Транспорт", "2023-06-04", "Автобус", False),
]

print("---")


transactions.append(
    Expense(600, "Продукти", "2023-06-05", "Овочі", False)
)

transactions.append(
    Expense(1100, "Розваги", "2023-10-05", "Танці", True)
)


for budget in budgets:
    budget.display_budget()
    budget.check_budget(transactions)
    budget.monthly_report(transactions)
    print()
    print("---")



