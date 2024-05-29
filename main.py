import asyncio

import coloredlogs
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka
from tortoise import Tortoise

from src.application import handlers, dialogs
from src.data.config import *
from src.impl.di import DefaultProvider


async def main():
    coloredlogs.install()

    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()

    bot = Bot(token=BOT_TOKEN, default=BOT_DEFAULT)
    dp = Dispatcher(storage=DISPATCHER_STORAGE, events_isolation=DISPATCHER_EVENTS_ISOLATION)
    container = make_async_container(DefaultProvider())
    allowed_updates = dp.resolve_used_update_types()

    setup_dishka(container=container, router=dp, auto_inject=True)
    setup_dialogs(router=dp)
    dp.include_routers(handlers.router, dialogs.router)
    await dp.start_polling(
        bot,
        allowed_updates=allowed_updates,
    )


if __name__ == '__main__':
    asyncio.run(main())
