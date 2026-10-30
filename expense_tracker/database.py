import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "expenses.db"

def get_connection():
    """Створює підключення до бази даних SQLite."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def init_db():
    """Створює таблиці бази даних."""

    connection = get_connection()

    try:
        # Таблиця користувачів
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)

        # Таблиця транзакцій
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL
                    CHECK (transaction_type IN ('income', 'expense')),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)
 # Перевіряємо наявні стовпці таблиці transactions
        transaction_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(transactions)"
            )
        }

        # Додаємо поле variable, якщо його ще немає
        if "variable" not in transaction_columns:
            connection.execute("""
                ALTER TABLE transactions
                ADD COLUMN variable INTEGER NOT NULL DEFAULT 0
            """)

        # Додаємо поле is_recurring, якщо його ще немає
        if "is_recurring" not in transaction_columns:
            connection.execute("""
                ALTER TABLE transactions
                ADD COLUMN is_recurring INTEGER NOT NULL DEFAULT 0
            """)


        # Таблиця бюджетів
        connection.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                monthly_limit REAL NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()

    finally:
        connection.close()
        