from pydantic import BaseModel

# Создание сериализаторов
class TronAddressRequest(BaseModel):
    """Схема для входящего запроса (адрес кошелька)."""
    address: str

    class Config:
        json_schema_extra = {
            "example": {
                "address": "TYmwSFuFuiDZCtYsRFKPNrDqH9V8x7K4Da"
            }
        }

class TronWalletResponse(BaseModel):
    """Схема для ответа с данными кошелька."""
    id : int
    address: str
    balance_trx: float
    bandwidth: int
    energy: int

    class Config:
        """Позволяет конвертировать ORM-объект в JSON"""
        from_attributes = True