import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



# Завантаження налаштувань із .env
load_dotenv()

# Адреса PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не знайдено у файлі .env")


# Створення Engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)


# Фабрика сесій
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Основа для моделей SQLAlchemy
Base = declarative_base()

# Функція для отримання сесії (для dependency injection)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Функція для ініціалізації БД
def init_db():
    """Створити всі таблиці"""
    Base.metadata.create_all(bind=engine)
    print("✅ БД ініціалізована")

# Функція для очистки БД (для тестування)
def drop_db():
    """Видалити всі таблиці"""
    Base.metadata.drop_all(bind=engine)
    print("✅ БД очищена")