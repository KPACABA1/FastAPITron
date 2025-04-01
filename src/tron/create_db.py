from src.tron.database import engine, Base
from src.tron.models import TronWallet

def create_tables():
    """Создает все таблицы в БД."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Таблицы успешно созданы!")