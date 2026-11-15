# crud_operations.py

from datetime import date
from sqlalchemy.orm import Session
from models import User, Category, Transaction, TransactionType

class UserCRUD:
    """CRUD-операції для користувачів."""

    # ===== CREATE =====

    @staticmethod
    def create(
        session: Session,
        username: str,
        email: str,
        password_hash: str
    ) -> User:
        """Створити користувача."""

        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        try:
            session.add(user)
            session.commit()
            session.refresh(user)

        except Exception:
            session.rollback()
            raise

        return user

    # ===== READ =====

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> User | None:
        """Отримати користувача за ID."""

        return (
            session.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_username(
        session: Session,
        username: str
    ) -> User | None:
        """Отримати користувача за username."""

        return (
            session.query(User)
            .filter(User.username == username)
            .first()
        )

    @staticmethod
    def get_all(
        session: Session,
        skip: int = 0,
        limit: int = 10
    ) -> list[User]:
        """Отримати всіх користувачів із пагінацією."""

        return (
            session.query(User)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ===== UPDATE =====

    @staticmethod
    def update(
        session: Session,
        user_id: int,
        **kwargs
    ) -> User | None:
        """Оновити дані користувача."""

        user = UserCRUD.get_by_id(session, user_id)

        if user is None:
            return None

        # Дозволені для зміни поля
        allowed_fields = {
            "username",
            "email",
            "password_hash",
            "currency"
        }

        try:
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(user, key, value)

            session.commit()
            session.refresh(user)

        except Exception:
            session.rollback()
            raise

        return user

    # ===== DELETE =====

    @staticmethod
    def delete(session: Session, user_id: int) -> bool:
        """Видалити користувача."""

        user = UserCRUD.get_by_id(session, user_id)

        if user is None:
            return False

        try:
            session.delete(user)
            session.commit()

        except Exception:
            session.rollback()
            raise

        return True

# ===== CATEGORY CRUD =====

class CategoryCRUD:
    """CRUD-операції для категорій."""

    @staticmethod
    def create(
        session: Session,
        name: str,
        category_type: TransactionType,
        user_id: int
    ) -> Category:
        """Створити категорію."""

        category = Category(
            name=name,
            type=category_type,
            user_id=user_id
        )

        try:
            session.add(category)
            session.commit()
            session.refresh(category)

        except Exception:
            session.rollback()
            raise

        return category

    @staticmethod
    def get_by_id(
        session: Session,
        category_id: int,
        user_id: int
    ) -> Category | None:
        """Отримати категорію за ID."""

        return (
            session.query(Category)
            .filter(
                Category.id == category_id,
                Category.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        session: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> list[Category]:
        """Отримати всі категорії користувача."""

        return (
            session.query(Category)
            .filter(Category.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        session: Session,
        category_id: int,
        user_id: int,
        **kwargs
    ) -> Category | None:
        """Оновити категорію."""

        category = CategoryCRUD.get_by_id(
            session, category_id, user_id
        )

        if category is None:
            return None

        allowed_fields = {"name", "type"}

        if any(key not in allowed_fields for key in kwargs):
            raise ValueError("Недозволене поле для оновлення категорії")

        if "type" in kwargs:
            new_type = kwargs["type"]

            # Не дозволяємо змінювати тип категорії,
            # якщо до неї вже прив'язані транзакції іншого типу.
            conflicting_transaction = (
                session.query(Transaction)
                .filter(
                    Transaction.category_id == category_id,
                    Transaction.transaction_type != new_type
                )
                .first()
            )

            if conflicting_transaction:
                raise ValueError(
                    "Неможливо змінити тип категорії: "
                    "існують пов'язані транзакції іншого типу."
                )

        try:
            for key, value in kwargs.items():
                setattr(category, key, value)

            session.commit()
            session.refresh(category)

        except Exception:
            session.rollback()
            raise

        return category

    @staticmethod
    def delete(
        session: Session,
        category_id: int,
        user_id: int
    ) -> bool:
        """Видалити категорію."""

        category = CategoryCRUD.get_by_id(
            session, category_id, user_id
        )

        if category is None:
            return False

        try:
            session.delete(category)
            session.commit()

        except Exception:
            session.rollback()
            raise

        return True


# ===== TRANSACTION CRUD =====

class TransactionCRUD:
    """CRUD-операції для фінансових транзакцій."""

    @staticmethod
    def create(
        session: Session,
        amount: float,
        transaction_type: TransactionType,
        category_id: int,
        user_id: int,
        description: str | None = None,
        transaction_date: date | None = None
    ) -> Transaction:
        """Створити транзакцію."""

        if amount <= 0:
            raise ValueError("Сума транзакції має бути більшою за 0")

        # Перевіряємо, чи належить категорія користувачу
        category = (
            session.query(Category)
            .filter(
                Category.id == category_id,
                Category.user_id == user_id
            )
            .first()
        )

        if category is None:
            raise ValueError("Категорію не знайдено")

        # Тип транзакції має відповідати типу категорії
        if category.type != transaction_type:
            raise ValueError(
                "Тип транзакції не відповідає типу категорії"
            )

        transaction = Transaction(
            amount=amount,
            transaction_type=transaction_type,
            category_id=category_id,
            user_id=user_id,
            description=description
        )

        if transaction_date is not None:
            transaction.transaction_date = transaction_date

        try:
            session.add(transaction)
            session.commit()
            session.refresh(transaction)

        except Exception:
            session.rollback()
            raise

        return transaction

    @staticmethod
    def get_by_id(
        session: Session,
        transaction_id: int,
        user_id: int
    ) -> Transaction | None:
        """Отримати транзакцію за ID."""

        return (
            session.query(Transaction)
            .filter(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        session: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> list[Transaction]:
        """Отримати всі транзакції користувача."""

        return (
            session.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.transaction_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        session: Session,
        transaction_id: int,
        user_id: int,
        **kwargs
    ) -> Transaction | None:
        """Оновити транзакцію."""

        transaction = TransactionCRUD.get_by_id(
            session, transaction_id, user_id
        )

        if transaction is None:
            return None

        allowed_fields = {
            "amount",
            "transaction_type",
            "category_id",
            "description",
            "transaction_date"
        }

        if any(key not in allowed_fields for key in kwargs):
            raise ValueError("Недозволене поле для оновлення транзакції")

        new_amount = kwargs.get("amount", transaction.amount)

        if new_amount <= 0:
            raise ValueError("Сума транзакції має бути більшою за 0")

        new_type = kwargs.get(
            "transaction_type",
            transaction.transaction_type
        )

        new_category_id = kwargs.get(
            "category_id",
            transaction.category_id
        )

        category = (
            session.query(Category)
            .filter(
                Category.id == new_category_id,
                Category.user_id == user_id
            )
            .first()
        )

        if category is None:
            raise ValueError("Категорію не знайдено")

        if category.type != new_type:
            raise ValueError(
                "Тип транзакції не відповідає типу категорії"
            )

        try:
            for key, value in kwargs.items():
                setattr(transaction, key, value)

            session.commit()
            session.refresh(transaction)

        except Exception:
            session.rollback()
            raise

        return transaction

    @staticmethod
    def delete(
        session: Session,
        transaction_id: int,
        user_id: int
    ) -> bool:
        """Видалити транзакцію."""

        transaction = TransactionCRUD.get_by_id(
            session, transaction_id, user_id
        )

        if transaction is None:
            return False

        try:
            session.delete(transaction)
            session.commit()

        except Exception:
            session.rollback()
            raise

        return True
