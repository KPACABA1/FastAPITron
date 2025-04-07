from sqlalchemy import Column, Integer, String, Float
from src.tron.database import Base

# Создание модельки
class TronWallet(Base):
    """Модель для хранения данных кошелька."""
    __tablename__ = "tron_wallets"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    balance_trx = Column(Float)
    bandwidth = Column(Integer)
    energy = Column(Integer)
