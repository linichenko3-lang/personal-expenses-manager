#Expense Tracker

transactions = []
def add_income():
    amount = float(input("Введіть суму доходу: "))
    category = input("Введіть категорію: ")

    transaction = {
        "amount": amount,
        "type": "income",
        "category": category
    }

    transactions.append(transaction)
    print("Дохід додано!")

def add_expense():
    """Додає до списку транзакцій витрату."""
    amount = float(input("Введіть суму витрати: "))
    category = input("Введіть категорію: ")

    transaction = {
        "amount": amount,
        "type": "expense",
        "category": category
    }

    transactions.append(transaction)
    print("Витрата додана!")

def show_transactions():
    """Виводить список усіх транзакцій."""
    if not transactions:
        print("  Транзакцій немає.\n")
        return
    print("  Список транзакцій:")
    for i, transaction in enumerate(transactions, start=1):
        print(f"    {i}. {transaction['type'].capitalize()}: {transaction['amount']}")
    print()

def delete_transaction():
    """Видаляє транзакцію за її номером у списку."""
    if not transactions:
        print("  Транзакцій немає для видалення.\n")
        return
    show_transactions()
    while True:
        try:
            index = int(input("Введіть номер транзакції для видалення: ")) - 1
            if 0 <= index < len(transactions):
                removed = transactions.pop(index)
                print(f"Транзакція {removed['type']} на суму {removed['amount']} видалена.\n")
                return
            else:
                print(f"Помилка: введено некоректний номер. Спробуйте ще раз.\n")
        except ValueError:
            print("Помилка: введено не число. Спробуйте ще раз.\n")

def main():
    while True:
        print("\nТрекер витрат")
        print("1. Додати дохід")
        print("2. Додати витрату")
        print("3. Показати транзакції")
        print("4. Видалити транзакцію")
        print("5. Вийти")

        choice = input("Виберіть варіант: ")

        if choice == "1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_transactions()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            print("До побачення!")
            break
        else:
            print("Помилка операції: введено некоректний вибір. Спробуйте ще раз.\n")


if __name__ == "__main__":
    main()


