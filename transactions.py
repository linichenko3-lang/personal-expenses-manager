import os
import uuid

import psycopg

from config import load_env


# Завантажуємо налаштування з .env
load_env()

DSN = os.getenv("EXPENSE_TRACKER_DSN")


def demonstrate_transactions():
    """Демонструє роботу COMMIT та ROLLBACK у PostgreSQL."""

    if not DSN:
        print("❌ Не знайдено EXPENSE_TRACKER_DSN у файлі .env")
        return

    # Унікальний суфікс, щоб скрипт можна було запускати повторно
    token = uuid.uuid4().hex[:8]

    success_username = f"tanya_{token}"
    success_email = f"tanya_{token}@example.com"

    rollback_username = f"slava_{token}"
    duplicate_username = f"eve_{token}"
    rollback_email = f"slava_{token}@example.com"

    print("=== ТРАНЗАКЦІЇ EXPENSE TRACKER ===\n")

    # ===== ПРИКЛАД 1. УСПІШНА ТРАНЗАКЦІЯ =====

    print("1. Успішна транзакція:\n")

    try:
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:

                # Крок 1. Створюємо користувача
                cur.execute(
                    """
                    INSERT INTO users (username, email, currency)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                    """,
                    (success_username, success_email, "UAH")
                )

                user_id = cur.fetchone()[0]

                print("  ✓ Крок 1: користувача додано")

                # Крок 2. Створюємо категорію
                cur.execute(
                    """
                    INSERT INTO categories (name, user_id)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    ("Тестова категорія", user_id)
                )

                category_id = cur.fetchone()[0]

                print("  ✓ Крок 2: категорію додано")

                # Крок 3. Додаємо витрату
                cur.execute(
                    """
                    INSERT INTO transactions (
                        amount,
                        transaction_type,
                        category_id,
                        description,
                        user_id
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        100.00,
                        "expense",
                        category_id,
                        "Тестова транзакція",
                        user_id
                    )
                )

                print("  ✓ Крок 3: транзакцію додано")

                # COMMIT — зберігаємо всі три операції
                conn.commit()

                print("  ✓ COMMIT: усі зміни збережені\n")

    except psycopg.Error as error:
        print(f"  ❌ Помилка: {error}\n")
        return

    # ===== ПРИКЛАД 2. ПОМИЛКА ТА ROLLBACK =====

    print("2. Транзакція з помилкою (ROLLBACK):\n")

    try:
        with psycopg.connect(DSN) as conn:
            try:
                with conn.cursor() as cur:

                    # Крок 1. Додаємо користувача
                    cur.execute(
                        """
                        INSERT INTO users (username, email)
                        VALUES (%s, %s);
                        """,
                        (rollback_username, rollback_email)
                    )

                    print("  ✓ Крок 1: користувача david додано")

                    # Крок 2. Спробуємо додати іншого
                    # користувача з таким самим email
                    cur.execute(
                        """
                        INSERT INTO users (username, email)
                        VALUES (%s, %s);
                        """,
                        (duplicate_username, rollback_email)
                    )

                    print("  Цей рядок не повинен виконатися")

                conn.commit()

            except psycopg.IntegrityError as error:

                # ROLLBACK скасовує обидва INSERT
                conn.rollback()

                print(f"  ❌ Помилка унікальності: {error}")
                print("  ↻ ROLLBACK: обидві операції скасовані\n")

    except psycopg.Error as error:
        print(f"  ❌ Помилка підключення: {error}\n")
        return

    # ===== ПРИКЛАД 3. ПЕРЕВІРКА РЕЗУЛЬТАТІВ =====

    print("3. Перевірка результатів:\n")

    try:
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:

                # Перевіряємо успішну транзакцію
                cur.execute(
                    """
                    SELECT
                        u.username,
                        u.email,
                        c.name,
                        t.amount,
                        t.transaction_type
                    FROM users u
                    JOIN categories c ON c.user_id = u.id
                    JOIN transactions t ON t.category_id = c.id
                    WHERE u.id = %s;
                    """,
                    (user_id,)
                )

                result = cur.fetchone()

                if result:
                    print("  ✅ Успішна транзакція збережена:")
                    print(f"     Користувач: {result[0]}")
                    print(f"     Категорія: {result[2]}")
                    print(f"     Сума: {result[3]} UAH")
                else:
                    print("  ❌ Дані не знайдені")

                # Перевіряємо користувачів після ROLLBACK
                cur.execute(
                    """
                    SELECT username
                    FROM users
                    WHERE username IN (%s, %s);
                    """,
                    (rollback_username, duplicate_username)
                )

                rollback_users = cur.fetchall()

                if not rollback_users:
                    print("\n  ✅ David і Eve відсутні в базі.")
                    print("  ✅ ROLLBACK спрацював правильно.")
                else:
                    print("\n  ❌ Знайдено записи після ROLLBACK.")

                print(
                    "\n  Успішний тестовий користувач:",
                    success_username
                )
                print(
                    "  Його email:",
                    success_email
                )

    except psycopg.Error as error:
        print(f"  ❌ Помилка перевірки: {error}")


if __name__ == "__main__":
    demonstrate_transactions()
