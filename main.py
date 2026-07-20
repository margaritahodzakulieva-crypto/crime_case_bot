import asyncio
from aiogram import Bot,Dispatcher

from handlers import router

from database.models import async_main


BOT_TOKEN = '8864138811:AAEWIE5mgddDjMWhJo2EKAei24VrkQaWKCA'


async def main():
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass