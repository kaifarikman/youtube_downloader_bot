import sys
import logging
import asyncio

from aiogram import Dispatcher

import bot.db.db as db
from bot.bot import bot
from bot.handlers import router


async def main():
    db.create_tables()
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except Exception as exception:
        print(f"Exit! - {exception}")
