import os
import psycopg

from config import load_env


# Завантажуємо налаштування з .env
load_env()

DSN = os.getenv("EXPENSE_TRACKER_DSN")


def analyze_database():
    """Аналізує структуру БД через information_schema."""

    if not DSN:
        print("❌ Не знайдено EXPENSE_TRACKER_DSN у файлі .env")
        return

    try:
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:

                print("=== АНАЛІЗ СТРУКТУРИ БД ===\n")

                # Отримуємо список таблиць
                print("📊 Таблиці:\n")

                cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                        AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                """)

                tables = cur.fetchall()

                if not tables:
                    print("Таблиць не знайдено.")
                    return

                for table in tables:
                    table_name = table[0]

                    print(f"📋 {table_name}")

                    # Отримуємо стовпці конкретної таблиці
                    cur.execute("""
                        SELECT
                            column_name,
                            data_type,
                            is_nullable
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                            AND table_name = %s
                        ORDER BY ordinal_position;
                    """, (table_name,))

                    columns = cur.fetchall()

                    for col_name, data_type, is_nullable in columns:

                        nullable = (
                            "NULL" if is_nullable == "YES"
                            else "NOT NULL"
                        )

                        print(
                            f"    • {col_name}: "
                            f"{data_type} [{nullable}]"
                        )

                    print()

    except psycopg.Error as error:
        print(f"❌ Помилка PostgreSQL: {error}")


if __name__ == "__main__":
    analyze_database()
    