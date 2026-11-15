import uuid

from database import SessionLocal
from models import TransactionType

from crud_operations import (
    UserCRUD,
    CategoryCRUD,
    TransactionCRUD,
)


# ==========================================
# USER CRUD
# ==========================================

def test_user_crud():
    """Тестування User CRUD."""

    print("\n=== TEST USER CRUD ===\n")

    session = SessionLocal()
    user = None

    # Унікальні дані, щоб тест можна було запускати повторно
    token = uuid.uuid4().hex[:8]
    username = f"ivan_test_{token}"
    email = f"ivan_{token}@test.com"

    try:
        # CREATE
        print("1. CREATE — додавання користувача")

        user = UserCRUD.create(
            session,
            username,
            email,
            "test_hash_123"
        )

        assert user.id is not None
        assert user.username == username

        print(f"✅ Користувач створений: ID {user.id}, {user.username}\n")

        # READ
        print("2. READ — отримання користувача")

        fetched = UserCRUD.get_by_username(session, username)

        assert fetched is not None
        assert fetched.email == email

        print(f"✅ Знайдено: {fetched.username} ({fetched.email})\n")

        # UPDATE
        print("3. UPDATE — оновлення користувача")

        new_email = f"ivan_new_{token}@test.com"

        updated = UserCRUD.update(
            session,
            user.id,
            email=new_email
        )

        assert updated is not None
        assert updated.email == new_email

        print(f"✅ Email оновлений: {updated.email}\n")

        # DELETE
        print("4. DELETE — видалення користувача")

        user_id = user.id
        deleted = UserCRUD.delete(session, user_id)

        assert deleted is True
        assert UserCRUD.get_by_id(session, user_id) is None

        print(f"✅ Користувач видалений: {deleted}\n")

    finally:
        # Прибираємо тестові дані, навіть якщо тест завершився помилкою
        session.rollback()

        if user is not None:
            existing_user = UserCRUD.get_by_id(session, user.id)

            if existing_user is not None:
                UserCRUD.delete(session, user.id)

        session.close()


# ==========================================
# CATEGORY CRUD
# ==========================================

def test_category_crud():
    """Тестування Category CRUD."""

    print("\n=== TEST CATEGORY CRUD ===\n")

    session = SessionLocal()
    user = None

    token = uuid.uuid4().hex[:8]

    try:
        # Створюємо користувача для категорії
        user = UserCRUD.create(
            session,
            f"category_user_{token}",
            f"category_{token}@test.com",
            "test_hash"
        )

        # CREATE
        print("1. CREATE — додавання категорії")

        category = CategoryCRUD.create(
            session,
            name="Їжа",
            category_type=TransactionType.EXPENSE,
            user_id=user.id
        )

        assert category.id is not None
        assert category.name == "Їжа"

        print(f"✅ Категорія створена: ID {category.id}, {category.name}\n")

        # READ
        print("2. READ — отримання категорії")

        fetched = CategoryCRUD.get_by_id(
            session,
            category.id,
            user.id
        )

        assert fetched is not None
        assert fetched.type == TransactionType.EXPENSE

        print(f"✅ Знайдено категорію: {fetched.name}\n")

        # READ ALL
        print("3. READ ALL — список категорій")

        categories = CategoryCRUD.get_all(
            session,
            user_id=user.id
        )

        assert len(categories) == 1

        print(f"✅ Кількість категорій: {len(categories)}\n")

        # UPDATE
        print("4. UPDATE — оновлення категорії")

        updated = CategoryCRUD.update(
            session,
            category.id,
            user.id,
            name="Продукти"
        )

        assert updated is not None
        assert updated.name == "Продукти"

        print(f"✅ Нова назва: {updated.name}\n")

        # DELETE
        print("5. DELETE — видалення категорії")

        category_id = category.id

        deleted = CategoryCRUD.delete(
            session,
            category_id,
            user.id
        )

        assert deleted is True
        assert CategoryCRUD.get_by_id(
            session,
            category_id,
            user.id
        ) is None

        print(f"✅ Категорія видалена: {deleted}\n")

    finally:
        session.rollback()

        if user is not None:
            existing_user = UserCRUD.get_by_id(session, user.id)

            if existing_user is not None:
                UserCRUD.delete(session, user.id)

        session.close()


# ==========================================
# TRANSACTION CRUD
# ==========================================

def test_transaction_crud():
    """Тестування Transaction CRUD."""

    print("\n=== TEST TRANSACTION CRUD ===\n")

    session = SessionLocal()
    user = None

    token = uuid.uuid4().hex[:8]

    try:
        # Створюємо користувача
        user = UserCRUD.create(
            session,
            f"transaction_user_{token}",
            f"transaction_{token}@test.com",
            "test_hash"
        )

        # Створюємо категорію витрат
        category = CategoryCRUD.create(
            session,
            name="Їжа",
            category_type=TransactionType.EXPENSE,
            user_id=user.id
        )

        # CREATE
        print("1. CREATE — додавання транзакції")

        transaction = TransactionCRUD.create(
            session,
            amount=350.00,
            transaction_type=TransactionType.EXPENSE,
            category_id=category.id,
            user_id=user.id,
            description="Обід у кафе"
        )

        assert transaction.id is not None
        assert transaction.amount == 350.00

        print(
            f"✅ Транзакція створена: ID {transaction.id}, "
            f"сума {transaction.amount} UAH\n"
        )

        # READ
        print("2. READ — отримання транзакції")

        fetched = TransactionCRUD.get_by_id(
            session,
            transaction.id,
            user.id
        )

        assert fetched is not None
        assert fetched.description == "Обід у кафе"

        print(
            f"✅ Знайдено: {fetched.description}, "
            f"{fetched.amount} UAH\n"
        )

        # READ ALL
        print("3. READ ALL — список транзакцій")

        transactions = TransactionCRUD.get_all(
            session,
            user_id=user.id
        )

        assert len(transactions) == 1

        print(f"✅ Кількість транзакцій: {len(transactions)}\n")

        # UPDATE
        print("4. UPDATE — оновлення транзакції")

        updated = TransactionCRUD.update(
            session,
            transaction.id,
            user.id,
            amount=500.00,
            description="Оновлена витрата"
        )

        assert updated is not None
        assert updated.amount == 500.00
        assert updated.description == "Оновлена витрата"

        print(
            f"✅ Оновлено: {updated.description}, "
            f"{updated.amount} UAH\n"
        )

        # DELETE
        print("5. DELETE — видалення транзакції")

        transaction_id = transaction.id

        deleted = TransactionCRUD.delete(
            session,
            transaction_id,
            user.id
        )

        assert deleted is True
        assert TransactionCRUD.get_by_id(
            session,
            transaction_id,
            user.id
        ) is None

        print(f"✅ Транзакція видалена: {deleted}\n")

    finally:
        session.rollback()

        if user is not None:
            existing_user = UserCRUD.get_by_id(session, user.id)

            if existing_user is not None:
                UserCRUD.delete(session, user.id)

        session.close()



if __name__ == "__main__":
    test_user_crud()
    test_transaction_crud()
    test_category_crud()
    

    print("\n✅ Все тести пройшли успішно!")

