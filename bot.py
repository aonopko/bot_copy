import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
claude = Anthropic(api_key=CLAUDE_API_KEY)

class PostStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_topic = State()
    waiting_for_photo = State()

# Создаем клавиатуру выбора языка
language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="Українська", callback_data="lang_ua")
    ]
])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Выберите язык для создания поста:", reply_markup=language_keyboard)

@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def process_language_selection(callback: types.CallbackQuery, state: FSMContext):
    language = callback.data.split('_')[1]
    await state.update_data(language=language)
    
    if language == 'ru':
        await callback.message.answer("Введите тему для поста на русском языке:")
    else:
        await callback.message.answer("Введіть тему для поста українською мовою:")
    
    await state.set_state(PostStates.waiting_for_topic)
    await callback.answer()

@dp.message(PostStates.waiting_for_topic)
async def process_topic(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data['language']
    
    # Формируем промпт для Claude в зависимости от выбранного языка
    if language == 'ru':
        prompt = f"Напиши привлекательный пост для социальной сети на тему: {message.text}. Пост должен быть на русском языке."
    else:
        prompt = f"Напиши привабливий пост для соціальної мережі на тему: {message.text}. Пост повинен бути українською мовою."

    # Получаем ответ от Claude
    response = claude.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    generated_post = response.content[0].text

    # Создаем клавиатуру для управления постом
    post_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить фото", callback_data="add_photo")],
        [InlineKeyboardButton(text="Опубликовать", callback_data="publish")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ])

    # Сохраняем пост в состояние
    await state.update_data(post_text=generated_post)
    
    # Отправляем пост пользователю с кнопками управления
    await message.answer(generated_post, reply_markup=post_keyboard)

@dp.callback_query(lambda c: c.data == "add_photo")
async def process_add_photo(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, отправьте фото для поста:")
    await state.set_state(PostStates.waiting_for_photo)
    await callback.answer()

@dp.message(PostStates.waiting_for_photo)
async def process_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фото (не файл).")
        return

    data = await state.get_data()
    post_text = data['post_text']

    post_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опубликовать", callback_data="publish")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ])

    # Сохраняем photo_id
    await state.update_data(photo_id=message.photo[-1].file_id)
    
    # Отправляем сообщение с фото и текстом
    await message.answer_photo(
        photo=message.photo[-1].file_id,
        caption=post_text,
        reply_markup=post_keyboard
    )

@dp.callback_query(lambda c: c.data == "publish")
async def process_publish(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    post_text = data['post_text']
    photo_id = data.get('photo_id')

    try:
        if photo_id:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo_id,
                caption=post_text
            )
        else:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=post_text
            )
        await callback.answer("Пост успешно опубликован!")
    except Exception as e:
        await callback.answer(f"Ошибка при публикации: {str(e)}")

@dp.callback_query(lambda c: c.data == "delete")
async def process_delete(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer("Пост удален!")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())