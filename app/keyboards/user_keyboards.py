from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks import ProfileCallback

def get_main_menu(user=None):
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Профиль", callback_data=ProfileCallback(action="profile"))
    builder.button(text="🛍️ Каталог", callback_data=ProfileCallback(action="catalog"))
    
    if user and user.can_manage_users():
        builder.button(text="👥 Управление сотрудниками", callback_data=ProfileCallback(action="user_management"))
    
    return builder.as_markup()

def get_profile_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Редактировать", callback_data=ProfileCallback(action="edit"))
    builder.button(text="🔙 Назад", callback_data=ProfileCallback(action="back"))
    return builder.as_markup()

def get_profile_edit_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Изменить имя", callback_data=ProfileCallback(action="edit_name"))
    builder.button(text="🎂 Изменить дату рождения", callback_data=ProfileCallback(action="edit_birth_date"))
    builder.button(text="🔙 Назад", callback_data=ProfileCallback(action="profile"))
    builder.adjust(1)
    return builder.as_markup()