from database import Base, init_db

# Імпортуємо моделі, щоб SQLAlchemy зареєструвала таблиці
from models import User, Category, Transaction, Budget


if __name__ == "__main__":
    print("🔄 Ініціалізація БД...")

    # Створюємо таблиці
    init_db()

    print("✅ Таблиці успішно створені!")

    # Перевіряємо створені таблиці
    print("\n📊 Створені таблиці:")

    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")