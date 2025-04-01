from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from src.tron.config import provider

# Действие для вьюшки(сервисная прослойка)
def get_tron_data(address: str) -> dict:
    """Получает данные кошелька из сети Tron."""
    try:
        client = Tron(provider=provider)

        # Проверка валидности адреса
        if not client.is_address(address):
            raise ValueError("Неверный адрес Tron")

        # Получаем аккаунт
        account = client.get_account(address)
        if not account:
            raise AddressNotFound("Адрес не найден")

        # Конвертируем баланс
        balance_trx = client.get_account_balance(address) / 1_000_000

        return {
            "address": address,
            "balance_trx": balance_trx,
            "bandwidth": account.get("free_net_limit", 0),
            "energy": account.get("energy_limit", 0)
        }
    except Exception as e:
        print(f"Ошибка: {e}")
