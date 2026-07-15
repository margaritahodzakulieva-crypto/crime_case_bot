import asyncio

from aiogram import Bot,Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


BOT_TOKEN = '8864138811:AAEWIE5mgddDjMWhJo2EKAei24VrkQaWKCA'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Hello!')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())