import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot,Dispatcher

from handlers import router
from database.models import async_main


load_dotenv()
bot_token = os.getenv("BOT_TOKEN")


async def main():
    await async_main()
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass