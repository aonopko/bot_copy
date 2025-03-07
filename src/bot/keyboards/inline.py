from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config.config import Config

def get_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="Українська", callback_data="lang_ua")
        ]
    ])

def get_post_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1500 символов", callback_data="type_1500")],
        [InlineKeyboardButton(text="1024 символа", callback_data="type_1024")]
    ])

def get_post_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить фото", callback_data="add_photo")],
        [InlineKeyboardButton(text="Опубликовать", callback_data="publish")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ])

def get_post_with_photo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опубликовать", callback_data="publish")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ]) 