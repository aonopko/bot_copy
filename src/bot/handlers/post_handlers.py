from aiogram import types
from aiogram.fsm.context import FSMContext
from src.bot.states.post_states import PostStates
from src.bot.keyboards.inline import get_post_keyboard, get_post_with_photo_keyboard
from src.bot.services.claude_service import ClaudeService
from config.config import Config

claude_service = ClaudeService(Config.CLAUDE_API_KEY)

async def register_post_handlers(dp):
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
        
        # Генерируем пост стандартной длины (500 символов)
        generated_post = await claude_service.generate_post(
            topic=message.text,
            language=data['language']
        )
        
        # Сохраняем пост в состояние
        await state.update_data(post_text=generated_post)
        
        # Отправляем пост с кнопками управления
        await message.answer(
            generated_post,
            reply_markup=get_post_keyboard()
        )

    @dp.callback_query(lambda c: c.data == "add_photo")
    async def process_add_photo(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Пожалуйста, отправьте фото для поста:")
        await state.set_state(PostStates.waiting_for_photo)
        await callback.answer()

    @dp.message(PostStates.waiting_for_photo)
    async def process_photo(message: types.Message, state: FSMContext):
        if not message.photo:
            await message.answer("Пожалуйста, отправьте изображение (не файл).")
            return

        data = await state.get_data()
        post_text = data['post_text']
        
        await state.update_data(photo_id=message.photo[-1].file_id)
        
        # Отправляем сообщение с фото и текстом
        await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption=post_text,
            reply_markup=get_post_with_photo_keyboard()
        )

    @dp.callback_query(lambda c: c.data == "publish")
    async def process_publish(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        post_text = data['post_text']
        photo_id = data.get('photo_id')

        try:
            if photo_id:
                await callback.bot.send_photo(
                    chat_id=Config.CHANNEL_ID,
                    photo=photo_id,
                    caption=post_text
                )
            else:
                await callback.bot.send_message(
                    chat_id=Config.CHANNEL_ID,
                    text=post_text
                )
            await callback.answer("Пост успешно опубликован!")
            await state.clear()
        except Exception as e:
            await callback.answer(f"Ошибка при публикации: {str(e)}")

    @dp.callback_query(lambda c: c.data == "delete")
    async def process_delete(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.delete()
        await callback.answer("Пост удален!")
        await state.clear() 