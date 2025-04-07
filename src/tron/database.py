from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.tron.config import DATABASE_URL


# Базовый класс для моделей
Base = declarative_base()

# Подключение к БД
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Сессии для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Базовый класс для моделей
# Base = declarative_base()