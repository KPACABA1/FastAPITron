from fastapi import FastAPI, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session
from src.tron import schemas, services, models
from src.tron.database import SessionLocal

app = FastAPI(title="Tron Info API")


# Зависимость для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/wallet", response_model=schemas.TronWalletResponse)
def fetch_wallet(
        request: schemas.TronAddressRequest,
        db: Session = Depends(get_db)
):
    """Получает данные кошелька и сохраняет в БД."""
    # Получаем данные из Tron
    tron_data = services.get_tron_data(request.address)
    # Сохраняем в БД
    db_wallet = models.TronWallet(**tron_data)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)

    return db_wallet


@app.get("/api/wallets", response_model=list[schemas.TronWalletResponse])
def list_wallets(
        # Пагинация
        skip: int = Query(0, ge=0),  # Пропустить N элементов (по умолчанию 0)
        limit: int = Query(5, le=100),  # Вернуть 5 элементов (макс. 100)
        db: Session = Depends(get_db)
):
    """Возвращает последние добавленные кошельки."""
    return db.query(models.TronWallet).order_by(desc(models.TronWallet.id)).offset(skip).limit(limit).all()