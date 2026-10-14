#Expense Tracker

class Transaction:
    def __init__(self, amount, category, date, description):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description


    def display_transaction(self):
            print(f"Cума: {self.amount}")
            print(f"Категорія: {self.category}")
            print(f"Дата: {self.date}")
            print(f"Опис: {self.description}")

    def display_income(self):
        print(f"Змінна: {self.variable}")


    def display_expense(self):
        print(f"Регулярна витрата: {self.is_recurring}")


    def calculate_balance(self):
        if isinstance(self, Income):
            return self.amount
        elif isinstance(self, Expense):
            return -self.amount
        else:
            return 0


class Income(Transaction):
    def __init__(self, amount, category, date, description, variable):
        super().__init__(amount, category, date, description)
        self.variable = variable


    def display_transaction(self):
        super().display_transaction()
        print(f"Змінна: {self.variable}")

class Expense(Transaction):
    def __init__(self, amount, category, date, description, is_recurring):
        super().__init__(amount, category, date, description)
        self.is_recurring = is_recurring

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


transaction = Income(10000, "Зарплата", "2023-06-01", "Місячна зарплата", True)

transaction.display_transaction()

print("---")

transaction1 = Expense(8000, "Харчування", "2023-06-02", "Молочні продукти", True)

transaction2 = Expense(3000, "Розваги", "2023-06-03", "Кінотеатр", True)

transaction.display_transaction()

print("---")

transaction1.display_transaction()

print(f"Баланс: {transaction1.calculate_balance()}")
print(f"Баланс: {transaction.calculate_balance()}")
print(f"Баланс: {transaction2.calculate_balance()}")

budgets = [
    Budget("Продукти", 2000),
    Budget("Розваги", 1500),
    Budget("Транспорт", 1000),
]

for budget in budgets:
    budget.display_budget()

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
    budget.check_budget([transaction1])
    budget.check_budget([transaction])
    budget.check_budget([transaction2])

for budget in budgets:
    budget.display_budget()
    budget.check_budget(transactions)
    print("---")

    budget.monthly_report(transactions)
    print()




