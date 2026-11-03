from datetime import datetime
import logging
from config import get_settings
from cli import build_parser


def configure_logging(settings):
    """Налаштовує логування застосунку."""

    log_level = getattr(
        logging,
        settings["log_level"].upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(
                "expense_tracker.log",
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )


def normalize_category(category, transaction_type):
    """Перетворює англійські назви категорій на українські."""

    if transaction_type == "income":
        categories = {
            "salary": "Зарплата",
            "bonus": "Премія",
            "freelance": "Фриланс",
            "investments": "Інвестиції",
            "other": "Інше",
        }
    else:
        categories = {
            "food": "Їжа",
            "rent": "Оренда",
            "utilities": "Комунальні послуги",
            "transport": "Транспорт",
            "health": "Здоров'я",
            "entertainment": "Розваги",
            "education": "Освіта",
            "clothing": "Одяг",
            "other": "Інше",
        }

    return categories.get(category.strip().lower(), category)


def main():
    # Створюємо парсер команд
    parser = build_parser()

    # Отримуємо аргументи командного рядка
    args = parser.parse_args()

    # Завантажуємо налаштування
    settings = get_settings()

    # Налаштовуємо логування
    configure_logging(settings)

    logging.debug("Запуск Expense & Budget Tracker")

    # Поки реалізуємо команду add
    if args.command == "add":

        if args.currency != settings["base_currency"]:
            parser.error(
                "Конвертація валюти ще не реалізована. "
                f"Доступна базова валюта: {settings['base_currency']}."
            )

        from expense_tracker.tracker import ExpenseTracker

        tracker = ExpenseTracker()

        category = normalize_category(
            args.category,
            args.transaction_type,
        )

        try:
            if args.transaction_type == "income":
                transaction = tracker.add_income(
                    amount=args.amount,
                    category=category,
                    description=args.desc,
                    transaction_date=args.date,
                )

            else:
                transaction = tracker.add_expense(
                    amount=args.amount,
                    category=category,
                    description=args.desc,
                    transaction_date=args.date,
                )

            if transaction is None:
                print("Транзакцію не додано. Перевірте суму.")
                return

            sign = "+" if args.transaction_type == "income" else "-"

            print(
                f"{sign}{args.amount:.2f} "
                f"{settings['base_currency']} "
                f"[{category}] додано."
            )

        except (ValueError, TypeError) as error:
            logging.warning("Помилка введення: %s", error)
            print(f"Помилка: {error}")

    elif args.command == "list":
        from expense_tracker.tracker import ExpenseTracker
        from expense_tracker.models import Income, Expense

        tracker = ExpenseTracker()
        transactions = tracker.transactions

        # Фільтр за типом транзакції
        if args.transaction_type == "income":
            transactions = [
                t for t in transactions
                if isinstance(t, Income)
            ]

        elif args.transaction_type == "expense":
            transactions = [
                t for t in transactions
                if isinstance(t, Expense)
            ]

        # Фільтр за категорією
        if args.category:
            transactions = [
                t for t in transactions
                if t.category.casefold() == args.category.casefold()
            ]

        # Фільтр за місяцем
        if args.month:
            try:
                datetime.strptime(args.month, "%Y-%m")
            except ValueError:
                parser.error("Місяць повинен мати формат YYYY-MM.")

            transactions = [
                t for t in transactions
                if t.date.startswith(args.month)
            ]

        # Сортування
        if args.sort == "amount":
            transactions = sorted(
                transactions,
                key=lambda t: t.amount,
                reverse=True,
            )
        else:
            transactions = sorted(
                transactions,
                key=lambda t: t.date,
                reverse=True,
            )

        # Обмеження кількості записів
        if args.limit is not None:
            if args.limit <= 0:
                parser.error("--limit має бути більшим за нуль.")

            transactions = transactions[:args.limit]

        # Виведення
        print("\n=== ТРАНЗАКЦІЇ ===")

        if not transactions:
            print("Транзакцій не знайдено.")
        else:
            for transaction in transactions:
                is_income = isinstance(transaction, Income)

                transaction_type = "income" if is_income else "expense"
                sign = "+" if is_income else "-"

                transaction_id = getattr(
                    transaction,
                    "_db_id",
                    "?"
                )

                print(
                    f"[{transaction_id}] "
                    f"{transaction.date} | "
                    f"{transaction_type:<7} | "
                    f"{transaction.category:<22} | "
                    f"{sign}{transaction.amount:.2f} "
                    f"{settings['base_currency']}"
                )

                if transaction.description:
                    print(f"    Опис: {transaction.description}")

    elif args.command == "balance":
        from expense_tracker.tracker import ExpenseTracker
        from expense_tracker.models import get_balance

        tracker = ExpenseTracker()

        balance = get_balance(tracker.user_id)

        print("\n=== ЗАГАЛЬНИЙ БАЛАНС ===")
        print(
            f"Баланс: {balance:+.2f} "
            f"{settings['base_currency']}"
        )

    elif args.command == "report":
        from datetime import datetime
        from expense_tracker.tracker import ExpenseTracker

        tracker = ExpenseTracker()

        month_str = args.month or datetime.now().strftime("%Y-%m")

        try:
            report_date = datetime.strptime(month_str, "%Y-%m")

            if report_date.strftime("%Y-%m") != month_str:
                raise ValueError

        except ValueError:
            parser.error(
                "Місяць повинен мати формат YYYY-MM. "
                "Наприклад: 2026-11"
            )

        report = tracker.monthly_report(
            report_date.year,
            report_date.month,
        )

        print(f"\n=== ЗВІТ ЗА {month_str} ===")
        print(f"Доходи:  +{report['income']:.2f} UAH")
        print(f"Витрати: -{report['expenses']:.2f} UAH")
        print(f"Баланс:   {report['balance']:+.2f} UAH")
        print(
            f"Кількість транзакцій: "
            f"{len(report['transactions'])}"
        )

    elif args.command == "delete":
        from expense_tracker.tracker import ExpenseTracker
        from expense_tracker.exceptions import TransactionNotFoundError

        tracker = ExpenseTracker()

        try:
            tracker.delete_transaction(args.id)

            print(
                f"Транзакцію #{args.id} успішно видалено."
            )

        except TransactionNotFoundError as error:
            print(f"Помилка: {error}")

    elif args.command == "budget":

        if args.budget_command == "set":
            from expense_tracker.tracker import ExpenseTracker
            from expense_tracker.models import Budget

            tracker = ExpenseTracker()

            category = normalize_category(
                args.category,
                "expense",
            )

            try:
                budget = Budget(
                    category=category,
                    monthly_limit=args.limit,
                )

                tracker.add_budget(budget)

                print(
                    f"Бюджет для '{category}' встановлено: "
                    f"{args.limit:.2f} "
                    f"{settings['base_currency']}"
                )

            except (ValueError, TypeError) as error:
                print(f"Помилка: {error}")

        elif args.budget_command == "show":
            from expense_tracker.tracker import ExpenseTracker
            from expense_tracker.models import check_budget_status

            tracker = ExpenseTracker()

            budgets = check_budget_status(tracker.user_id)

            print("\n===== МОЇ БЮДЖЕТИ =====")

            if not budgets:
                print("Бюджети ще не встановлені.")
                return

            for budget in budgets:
                category = budget["category"]
                monthly_limit = budget["monthly_limit"]
                spent = budget["total_expenses"]

                remaining = monthly_limit - spent

                if monthly_limit > 0:
                    utilization = spent / monthly_limit * 100
                else:
                    utilization = 0.0

                print(f"\nКатегорія: {category}")
                print(f"Місячний ліміт: {monthly_limit:.2f} UAH")
                print(f"Витрачено: {spent:.2f} UAH")
                print(f"Залишок: {remaining:.2f} UAH")
                print(f"Використання бюджету: {utilization:.1f}%")

                if budget["exceeded"]:
                    print("УВАГА! Бюджет перевищено!")

                elif utilization >= settings["warn_budget_pct"]:
                    print("УВАГА! Ви наближаєтеся до ліміту!")


    elif args.command == "export":
        from expense_tracker.tracker import ExpenseTracker
        from expense_tracker.models import get_all_transactions
        from expense_tracker.storage import export_transactions

        tracker = ExpenseTracker()
        transactions = get_all_transactions(tracker.user_id)

        try:
            output_path = export_transactions(
                transactions,
                args.format,
                settings["export_dir"]
            )
            print(
                f"Експортовано {len(transactions)} транзакцій: "
                f"{output_path}"
            )
        except (OSError, ValueError) as error:
            parser.error(str(error))

    else:
        print(
            f"Команда '{args.command}' поки не підключена до SQLite."
        )

    


if __name__ == "__main__":
    main()
