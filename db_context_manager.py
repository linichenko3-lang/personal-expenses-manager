import os
from contextlib import contextmanager
from typing import Generator

import psycopg

from config import load_env


# Завантажуємо налаштування з .env
load_env()

DSN = os.getenv("EXPENSE_TRACKER_DSN")


@contextmanager
def get_db_connection(dsn: str) -> Generator:
    """
    Контекстний менеджер для безпечної роботи з БД.

    Використання:
        with get_db_connection(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users;")
    """

    with psycopg.connect(dsn) as conn:
        yield conn


@contextmanager
def get_db_cursor(dsn: str) -> Generator:
    """
    Контекстний менеджер для отримання курсора.

    Використання:
        with get_db_cursor(DSN) as cur:
            cur.execute("SELECT * FROM users;")
    """

    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            yield cur


def main():
    """Перевіряє роботу контекстних менеджерів."""

    if not DSN:
        print("❌ Не знайдено EXPENSE_TRACKER_DSN у файлі .env")
        return

    print("=== КОНТЕКСТНИЙ МЕНЕДЖЕР ===\n")

    try:
        # Варіант 1. Використання get_db_connection
        print("1. Використання get_db_connection:\n")

        with get_db_connection(DSN) as conn:
            with conn.cursor() as cur:

                cur.execute("SELECT COUNT(*) FROM users;")

                count = cur.fetchone()[0]

                print(f"  Всього користувачів: {count}\n")

        # Варіант 2. Використання get_db_cursor
        print("2. Використання get_db_cursor:\n")

        with get_db_cursor(DSN) as cur:

            cur.execute(
                "SELECT username FROM users LIMIT 3;"
            )

            users = cur.fetchall()

            for row in users:
                print(f"  - {row[0]}")

        print("\n✅ Роботу контекстних менеджерів перевірено.")

    except psycopg.Error as error:
        print(f"❌ Помилка PostgreSQL: {error}")


if __name__ == "__main__":
    main()