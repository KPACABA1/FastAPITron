import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

from src.tron.main import app, get_db
from src.tron.models import TronWallet, Base


# Настройка тестовой БД
@pytest.fixture(scope="function")
def test_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(test_db):
    def override_get_db():
        try:
            db = test_db()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_list_wallets(test_client, test_db):
    """Интеграционный тест на просмотр записанных результатов."""
    # Создание экземпляра модели
    db = test_db()
    direct_tron_wallet = TronWallet(address="address", balance_trx=123.9, bandwidth=123, energy=123)
    db.add(direct_tron_wallet)
    db.commit()
    tron_wallet_id = direct_tron_wallet.id
    db.close()

    # Делаем запрос
    response = test_client.get("/api/wallets")

    # Сами тесты с получением созданного экземпляра модели
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data[0]["id"] == tron_wallet_id
    assert data[0]["address"] == "address"
    assert data[0]["balance_trx"] == 123.9


# Создание готовой сессии для юнит теста
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(engine)


def test_db_wallet_creation(db_session):
    """Юнит-тест на запись экземпляра модели в БД"""
    # Создание экземпляра модели вручную
    wallet = TronWallet(address="address", balance_trx=123.9, bandwidth=123, energy=123)
    db_session.add(wallet)
    db_session.commit()

    # Получение созданного экземпляра модели
    db_wallet = db_session.query(TronWallet).filter(TronWallet.address == "address").first()

    # Тестирование
    assert db_wallet is not None
    assert db_wallet.balance_trx == 123.9
    assert db_wallet.bandwidth == 123