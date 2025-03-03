import asyncio
from aiogram import Bot, Dispatcher
from config.config import Config
from src.bot.handlers.common_handlers import register_common_handlers
from src.bot.handlers.post_handlers import register_post_handlers

async def main():
    Config.validate()
    
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация обработчиков
    await register_common_handlers(dp)
    await register_post_handlers(dp)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 