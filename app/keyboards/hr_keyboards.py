from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks import HrCallback, ProfileCallback

def get_hr_user_management_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="👥 Список активных", callback_data=HrCallback(action="active_users"))
    builder.button(text="👥 Список уволенных", callback_data=HrCallback(action="inactive_users"))
    builder.button(text="🔙 Назад", callback_data=ProfileCallback(action="back"))
    return builder.as_markup()

def get_hr_user_actions_menu(user_id: int, is_active: bool):
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✏️ Изменить данные", 
        callback_data=HrCallback(action="edit_user_info", user_id=user_id)
    )
    builder.button(
        text="💵 Начислить T-Point", 
        callback_data=HrCallback(action="add_tpoint", user_id=user_id)
    )
    
    if is_active:
        builder.button(
            text="🚫 Деактивировать", 
            callback_data=HrCallback(action="deactivate", user_id=user_id)
        )
    else:
        builder.button(
            text="✅ Активировать", 
            callback_data=HrCallback(action="activate", user_id=user_id)
        )
    
    builder.button(text="🔙 Назад", callback_data=HrCallback(action="user_list"))
    builder.adjust(1)
    return builder.as_markup()

def get_hr_edit_fields_menu(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Имя", callback_data=HrCallback(action="edit_name", user_id=user_id))
    builder.button(text="👔 Должность", callback_data=HrCallback(action="edit_position", user_id=user_id))
    builder.button(text="🏢 Отдел", callback_data=HrCallback(action="edit_department", user_id=user_id))
    builder.button(text="📅 Дата найма", callback_data=HrCallback(action="edit_hire_date", user_id=user_id))
    builder.button(text="🎂 Дата рождения", callback_data=HrCallback(action="edit_birth_date", user_id=user_id))
    builder.button(text="🔙 Назад", callback_data=HrCallback(action="user_info", user_id=user_id))
    builder.adjust(2)
    return builder.as_markup()