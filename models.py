from datetime import datetime, date
import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Date,
)

from sqlalchemy.orm import relationship

from database import Base


# ===== ENUM =====

class TransactionType(str, enum.Enum):
    """Тип фінансової транзакції."""

    INCOME = "income"
    EXPENSE = "expense"


# ===== USER =====

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    currency = Column(String(3), default="UAH")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Зв'язки
    categories = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    transactions = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    budgets = relationship(
        "Budget",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ===== CATEGORY =====

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Зв'язки
    user = relationship("User", back_populates="categories")

    transactions = relationship(
        "Transaction",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    budgets = relationship(
        "Budget",
        back_populates="category",
        cascade="all, delete-orphan"
    )


# ===== TRANSACTION =====

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String(500))
    transaction_date = Column(Date, default=date.today)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Зв'язки
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


# ===== BUDGET =====

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    monthly_limit = Column(Float, nullable=False)
    month = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Зв'язки
    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")
