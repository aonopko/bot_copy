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
        generated_post = await claude_service.generate_post(message.text, data['language'])
        
        await state.update_data(post_text=generated_post)
        await message.answer(generated_post, reply_markup=get_post_keyboard())

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
        await state.update_data(photo_id=message.photo[-1].file_id)
        
        await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption=data['post_text'],
            reply_markup=get_post_with_photo_keyboard()
        )

    @dp.callback_query(lambda c: c.data == "publish")
    async def process_publish(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        try:
            if photo_id := data.get('photo_id'):
                await callback.bot.send_photo(
                    chat_id=Config.CHANNEL_ID,
                    photo=photo_id,
                    caption=data['post_text']
                )
            else:
                await callback.bot.send_message(
                    chat_id=Config.CHANNEL_ID,
                    text=data['post_text']
                )
            await callback.answer("Пост успешно опубликован!")
        except Exception as e:
            await callback.answer(f"Ошибка при публикации: {str(e)}")

    @dp.callback_query(lambda c: c.data == "delete")
    async def process_delete(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.delete()
        await callback.answer("Пост удален!")
        await state.clear() 