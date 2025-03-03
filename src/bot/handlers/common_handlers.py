from aiogram import types
from aiogram.filters import Command
from src.bot.keyboards.inline import get_language_keyboard

async def register_common_handlers(dp):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer(
            "Выберите язык для создания поста:", 
            reply_markup=get_language_keyboard()
        ) 