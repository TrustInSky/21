
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks import ProfileCallback

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Профиль", callback_data=ProfileCallback(action="profile"))
    return builder.as_markup()

def get_profile_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Редактировать", callback_data=ProfileCallback(action="edit"))
    builder.button(text="Назад", callback_data=ProfileCallback(action="back"))
    return builder.as_markup()