from expense_tracker.models import Income, Expense
from expense_tracker.tracker import ExpenseTracker
from expense_tracker.exceptions import (
    ExpenseTrackerError,
    InvalidAmountError,
    TransactionNotFoundError,
)
from expense_tracker.constants import IncomeCategory, ExpenseCategory

class ExpenseTrackerCLI:
    """Консольний інтерфейс для керування фінансами."""

    def __init__(self):
        self.tracker = ExpenseTracker()

    def show_menu(self):
        print("\n===== EXPENSE TRACKER =====")
        print("1. Додати дохід")
        print("2. Додати витрату")
        print("3. Переглянути транзакції")
        print("4. Видалити транзакцію")
        print("5. Переглянути загальний баланс")
        print("6. Місячний звіт")
        print("0. Вийти")

    def add_transaction(self, transaction_type):
        try:
            amount = float(input("Введіть суму: "))

            if transaction_type == "income":
                category = self._read_category(IncomeCategory)
            else:
                category = self._read_category(ExpenseCategory)

            transaction_date = input("Дата (РРРР-ММ-ДД): ")
            description = input("Опис: ")

            if transaction_type == "income":
                variable = self._read_boolean(
                    "Дохід змінний? (так/ні): "
                )
                transaction = Income(
                    amount,
                    category,
                    transaction_date,
                    description,
                    variable,
                )
            else:
                is_recurring = self._read_boolean(
                    "Регулярна витрата? (так/ні): "
                )
                transaction = Expense(
                    amount,
                    category,
                    transaction_date,
                    description,
                    is_recurring,
                )

            self.tracker.add_transaction(transaction)
            print("Транзакцію успішно додано!")

        except ValueError as error:
            print(f"Помилка введення: {error}")
        except TypeError as error:
            print(f"Помилка типу даних: {error}")
        except ExpenseTrackerError as error:
            print(f"Помилка: {error}")


    @staticmethod
    def _read_category(category_enum):
        categories = list(category_enum)

        print("\nДоступні категорії:")

        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category.value}")

        choice = int(input("Оберіть номер категорії: "))

        if not 1 <= choice <= len(categories):
            raise ValueError("Категорії з таким номером немає.")

        return categories[choice - 1].value

    @staticmethod
    def _read_boolean(prompt):
        answer = input(prompt).strip().lower()

        if answer in ("так", "т", "так.", "yes", "y"):
            return True
        if answer in ("ні", "н", "no", "n"):
            return False

        raise ValueError("Введіть «так» або «ні».")

    def show_transactions(self):
        transactions = self.tracker.transactions

        if not transactions:
            print("Список транзакцій порожній.")
            return

        for index, transaction in enumerate(transactions, start=1):
            print(f"\nТранзакція №{index}")
            transaction.display_transaction()
            print(f"Вплив на баланс: {transaction.calculate_balance} грн")

    def delete_transaction(self):
        self.show_transactions()

        transactions = self.tracker.transactions
        if not transactions:
            return

        try:
            number = int(input("\nВведіть номер транзакції для видалення: "))

            if not 1 <= number <= len(transactions):
                raise TransactionNotFoundError(
                    "Транзакції з таким номером немає."
                )

            self.tracker.delete_transaction(transactions[number - 1])
            print("Транзакцію успішно видалено!")

        except ValueError as error:
            print(f"Помилка введення: {error}")
        except TransactionNotFoundError as error:
            print(f"Помилка: {error}")

    def show_balance(self):
        balance = self.tracker.calculate_balance()
        print(f"Загальний баланс: {balance:.2f} грн")

    def show_monthly_report(self):
        try:
            year = int(input("Введіть рік, наприклад 2026: "))
            month = int(input("Введіть номер місяця (1–12): "))

            report = self.tracker.monthly_report(year, month)

            print(f"\n===== ЗВІТ ЗА {month:02d}.{year} =====")
            print(f"Доходи: {report['income']:.2f} грн")
            print(f"Витрати: {report['expenses']:.2f} грн")
            print(f"Баланс за місяць: {report['balance']:.2f} грн")
            print(
                f"Кількість транзакцій: "
                f"{len(report['transactions'])}"
            )

        except ValueError as error:
            print(f"Помилка введення: {error}")
        except TypeError as error:
            print(f"Помилка типу даних: {error}")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Оберіть дію: ").strip()

            if choice == "1":
                self.add_transaction("income")
            elif choice == "2":
                self.add_transaction("expense")
            elif choice == "3":
                self.show_transactions()

            elif choice == "4":
                self.delete_transaction()

            elif choice == "5":
                self.show_balance()
            elif choice == "6":
                self.show_monthly_report()
            elif choice == "0":
                print("Роботу Expense Tracker завершено.")
                break
            else:
                print("Невідома команда. Спробуйте ще раз.")


