from typing import Final
from tronpy.providers import HTTPProvider
import os
from dotenv import load_dotenv

load_dotenv()

# Конфиг для Tron
TRON_NODE: Final[str] = "https://api.trongrid.io"  # Официальная нода
# Создаём HTTPProvider
provider = HTTPProvider(TRON_NODE, api_key=os.getenv('api_key'))

# Настройки БД (SQLite)
DATABASE_URL: Final[str] = "sqlite:///./tron.db"