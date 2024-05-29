from pathlib import Path

import pytz as pytz
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from environs import Env

BASE_DIR = Path(__file__).parent.parent.parent

env = Env()
env.read_env()

# Получаем конфиги
BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN_IDS = list(map(int, env.list('ADMIN_IDS')))

# Настраиваем конфигурацию бота
BOT_DEFAULT = DefaultBotProperties(
    parse_mode=ParseMode.HTML,
)
DISPATCHER_STORAGE = MemoryStorage()
DISPATCHER_EVENTS_ISOLATION = SimpleEventIsolation()

# Настройка базы данных
DATABASE_PATH = BASE_DIR / 'db.sqlite3'
DATABASE_CONFIG = {
    "connections": {
        "default": f"sqlite:///{DATABASE_PATH}"
    },
    "apps": {
        "models": {
            "models": ["src.domain.models"],
            "default_connection": "default",
        }
    },
}

# Настройка локализации
LOCALES_DIR = BASE_DIR / 'src' / 'data' / 'locales'
DEFAULT_LOCALE_NAME = 'ru'

# Настройка менеджера конфигурации
CONFIG_MANAGER_FILE = BASE_DIR / 'config.pkl'

# Используемый часовой пояс
TIME_ZONE = pytz.timezone('Europe/Moscow')
