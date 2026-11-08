import os
import psycopg
from psycopg import sql

from config import load_env


load_env()

# Параметри підключення
ADMIN_DSN = os.getenv("POSTGRES_ADMIN_DSN")
DSN = os.getenv("EXPENSE_TRACKER_DSN")

DB_NAME = "expense_tracker"


def create_database():
    """Створює базу даних Expense Tracker та таблиці."""

    if not ADMIN_DSN or not DSN:
        raise ValueError(
            "Не знайдено POSTGRES_ADMIN_DSN або EXPENSE_TRACKER_DSN у .env"
        )

    try:
        # Створення бази даних, якщо вона ще не існує
        with psycopg.connect(ADMIN_DSN, autocommit=True) as conn:
            with conn.cursor() as cur:

                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (DB_NAME,)
                )

                database_exists = cur.fetchone()

                if database_exists is None:
                    cur.execute(
                        sql.SQL("CREATE DATABASE {}").format(
                            sql.Identifier(DB_NAME)
                        )
                    )
                    print(f"✅ База даних {DB_NAME} створена")
                else:
                    print(f"ℹ️ База даних {DB_NAME} вже існує")

        # Створення таблиць
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:

                # Користувачі
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        currency VARCHAR(3) DEFAULT 'UAH',
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)

                # Категорії
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS categories (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id)
                            REFERENCES users(id) ON DELETE CASCADE
                    );
                """)

                # Транзакції
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id SERIAL PRIMARY KEY,
                        amount DECIMAL(10, 2) NOT NULL,
                        transaction_type VARCHAR(20) NOT NULL,
                        category_id INTEGER,
                        description TEXT,
                        user_id INTEGER NOT NULL,
                        transaction_date DATE DEFAULT CURRENT_DATE,
                        created_at TIMESTAMP DEFAULT NOW(),
                        FOREIGN KEY (category_id)
                            REFERENCES categories(id) ON DELETE SET NULL,
                        FOREIGN KEY (user_id)
                            REFERENCES users(id) ON DELETE CASCADE
                    );
                """)

                # Бюджети
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS budgets (
                        id SERIAL PRIMARY KEY,
                        category_id INTEGER NOT NULL,
                        monthly_limit DECIMAL(10, 2) NOT NULL,
                        month DATE NOT NULL,
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (category_id)
                            REFERENCES categories(id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id)
                            REFERENCES users(id) ON DELETE CASCADE
                    );
                """)

            # Контекстне керування з'єднанням автоматично виконає commit

        print(
            "✅ Таблиці створені: users, categories, "
            "transactions, budgets"
        )

    except psycopg.Error as error:
        print(f"❌ Помилка PostgreSQL: {error}")


if __name__ == "__main__":
    create_database()