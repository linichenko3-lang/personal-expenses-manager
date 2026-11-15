# migration_example.py
"""
Порівняння: "сирий" SQL vs SQLAlchemy ORM
"""
import inspect
from database import SessionLocal, engine
import psycopg
from models import User, Transaction


# psycopg 3 використовує звичайний PostgreSQL DSN.
# У DATABASE_URL у нас може бути драйвер postgresql+psycopg2.
PSYCOPG_DSN = engine.url.render_as_string(
    hide_password=False
).replace("postgresql+psycopg2://", "postgresql://", 1)


# =========================================================
# ❌ СТАРИЙ СПОСІБ — "сирий" SQL через psycopg
# =========================================================

def old_add_user_sql(username: str, email: str, password_hash: str):
    """Додавання користувача через SQL."""

    conn = psycopg.connect(PSYCOPG_DSN)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            """
            (username, email, password_hash)
        )
        conn.commit()
        print(f"✅ SQL: користувач {username} додан")

    finally:
        cur.close()
        conn.close()


def old_get_users_sql():
    """Отримання всіх користувачів через SQL."""

    conn = psycopg.connect(PSYCOPG_DSN)
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, username, email FROM users")
        rows = cur.fetchall()

        users = [
            {"id": row[0], "username": row[1], "email": row[2]}
            for row in rows
        ]

        return users

    finally:
        cur.close()
        conn.close()


def old_update_user_sql(user_id: int, email: str):
    """Оновлення email користувача через SQL."""

    conn = psycopg.connect(PSYCOPG_DSN)
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE users SET email = %s WHERE id = %s",
            (email, user_id)
        )
        conn.commit()
        print(f"✅ SQL: користувач {user_id} оновлений")

    finally:
        cur.close()
        conn.close()


def old_get_user_transactions_sql(user_id: int):
    """Отримання транзакцій користувача через SQL JOIN."""

    conn = psycopg.connect(PSYCOPG_DSN)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT u.username, t.amount, t.transaction_type
            FROM users u
            LEFT JOIN transactions t ON u.id = t.user_id
            WHERE u.id = %s
            """,
            (user_id,)
        )

        rows = cur.fetchall()
        return rows

    finally:
        cur.close()
        conn.close()



# =========================================================
# ✅ НОВИЙ СПОСІБ — SQLAlchemy ORM
# =========================================================

def new_add_user_orm(username: str, email: str, password_hash: str):
    """ORM версія."""

    session = SessionLocal()
    try:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        session.add(user)
        session.commit()

        print(f"✅ ORM: користувач {username} додан")

    finally:
        session.close()


def new_get_users_orm():
    """ORM версія."""

    session = SessionLocal()
    try:
        users = session.query(User).all()

        return [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email
            }
            for u in users
        ]

    finally:
        session.close()


def new_update_user_orm(user_id: int, email: str):
    """ORM версія."""

    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()

        if user:
            user.email = email
            session.commit()

            print(f"✅ ORM: користувач {user_id} оновлений")

    finally:
        session.close()


def new_get_user_transactions_orm(user_id: int):
    """ORM версія через relationship."""

    session = SessionLocal()
    try:
        user = session.query(User).filter_by(id=user_id).first()

        if user:
            # Прямий доступ до транзакцій через relationship!
            return [
                (
                    user.username,
                    transaction.amount,
                    transaction.transaction_type.name
                )
                for transaction in user.transactions
            ]

        return []

    finally:
        session.close()

# =========================================================
# ПОРІВНЯННЯ SQL vs ORM
# =========================================================

def compare_code(sql_function, orm_function):
    """Порівнює кількість рядків у SQL та ORM функціях."""

    sql_lines = len(inspect.getsource(sql_function).splitlines())
    orm_lines = len(inspect.getsource(orm_function).splitlines())

    saving = (sql_lines - orm_lines) / sql_lines * 100

    print(f"   SQL: {sql_lines} рядків")
    print(f"   ORM: {orm_lines} рядків")
    print(f"   Економія: {saving:.1f}%\n")


if __name__ == "__main__":

    print("=== ПОРІВНЯННЯ: SQL vs ORM ===\n")

    # ADD
    print("1. ADD USER")
    compare_code(old_add_user_sql, new_add_user_orm)

    # GET
    print("2. GET USERS")
    compare_code(old_get_users_sql, new_get_users_orm)

    # UPDATE
    print("3. UPDATE USER")
    compare_code(old_update_user_sql, new_update_user_orm)

    # JOIN
    print("4. GET USER WITH TRANSACTIONS")
    compare_code(
        old_get_user_transactions_sql,
        new_get_user_transactions_orm
    )

    print("✨ Висновок:")
    print("SQLAlchemy ORM спрощує роботу з базою даних.")
    print("Не потрібно вручну відкривати з'єднання,")
    print("створювати курсори та писати SQL-запити")
    print("для стандартних операцій CRUD.")
