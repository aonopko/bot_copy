from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="Українська", callback_data="lang_ua")
        ]
    ])

def get_post_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опубликовать с фото", callback_data="publish_with_photo")],
        [InlineKeyboardButton(text="Опубликовать без фото", callback_data="publish_without_photo")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ])

def get_post_with_photo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опубликовать", callback_data="publish")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ]) 