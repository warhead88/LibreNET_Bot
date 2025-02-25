import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import router
from database import Database

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    db = await Database.create()  # Инициализация базы данных

    dp["db"] = db  # Передаём объект базы данных в контекст aiogram

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
