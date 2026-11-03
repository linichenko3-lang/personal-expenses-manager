import argparse
from enum import Enum

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

class ExportFormat(Enum):
    CSV = "csv"
    JSON = "json"

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Expense & Budget Tracker — облік доходів і витрат",
        epilog=(
            "Приклад: python main.py add expense "
            "--amount 350 --category Food"
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Expense Tracker v0.3.0",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
    )
    subparsers.required = True

    # ---------- add ----------
    add_parser = subparsers.add_parser(
        "add",
        help="Додати транзакцію",
    )

    add_parser.add_argument(
        "transaction_type",
        choices=[t.value for t in TransactionType],
        help="Тип транзакції: income або expense",
    )

    add_parser.add_argument(
        "--amount",
        type=float,
        required=True,
        help="Сума транзакції",
    )

    add_parser.add_argument(
        "--category",
        required=True,
        help="Категорія",
    )

    add_parser.add_argument(
        "--desc",
        default="",
        help="Опис транзакції",
    )

    add_parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Дата транзакції (за замовчуванням: сьогодні)",
    )

    add_parser.add_argument(
        "--currency",
        default="UAH",
        choices=["UAH", "USD", "EUR"],
        help="Валюта транзакції",
    )

    # ---------- list ----------
    list_parser = subparsers.add_parser(
        "list",
        help="Переглянути транзакції",
    )

    list_parser.add_argument(
        "--type",
        dest="transaction_type",
        choices=[t.value for t in TransactionType],
        help="Фільтр за типом транзакції",
    )

    list_parser.add_argument(
        "--category",
        help="Фільтр за категорією",
    )

    list_parser.add_argument(
        "--month",
        metavar="YYYY-MM",
        help="Фільтр за місяцем",
    )

    list_parser.add_argument(
        "--sort",
        choices=["date", "amount"],
        default="date",
        help="Сортування транзакцій",
    )

    list_parser.add_argument(
        "--limit",
        type=int,
        help="Максимальна кількість транзакцій",
    )

    # ---------- balance ----------
    subparsers.add_parser(
        "balance",
        help="Показати поточний баланс",
    )

    # ---------- report ----------
    report_parser = subparsers.add_parser(
        "report",
        help="Місячний звіт",
    )

    report_parser.add_argument(
        "--month",
        metavar="YYYY-MM",
        help="Місяць звіту",
    )

    # ---------- delete ----------
    delete_parser = subparsers.add_parser(
        "delete",
        help="Видалити транзакцію",
    )

    delete_parser.add_argument(
        "--id",
        type=int,
        required=True,
        help="ID транзакції",
    )

    # ---------- budget ----------
    budget_parser = subparsers.add_parser(
        "budget",
        help="Керування бюджетами",
    )

    budget_sub = budget_parser.add_subparsers(
        dest="budget_command",
        metavar="SUBCOMMAND",
    )
    budget_sub.required = True

    budget_set = budget_sub.add_parser(
        "set",
        help="Встановити бюджет",
    )

    budget_set.add_argument(
        "--category",
        required=True,
        help="Категорія",
    )

    budget_set.add_argument(
        "--limit",
        type=float,
        required=True,
        help="Місячний ліміт",
    )

    budget_sub.add_parser(
        "show",
        help="Переглянути бюджети",
    )

    # ---------- export ----------
    export_parser = subparsers.add_parser(
        "export",
        help="Експортувати дані",
    )

    export_parser.add_argument(
        "--format",
        choices=[f.value for f in ExportFormat],
        default=ExportFormat.CSV.value,
        help="Формат експорту",
    )

    return parser