from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.callbacks import AdminCallback, ProfileCallback

def get_admin_user_management_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="👥 Список активных", callback_data=AdminCallback(action="active_users"))
    builder.button(text="👥 Список уволенных", callback_data=AdminCallback(action="inactive_users"))
    builder.button(text="🔙 Назад", callback_data=ProfileCallback(action="back"))
    builder.adjust(1)
    return builder.as_markup()

def get_user_list_markup(users: list, show_active: bool = True, page: int = 0, per_page: int = 10):
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки пользователей (имя или username)
    for user in users[page * per_page: (page + 1) * per_page]:
        builder.button(
            text=f"{user.name or user.username or f'ID {user.telegram_id}'}",
            callback_data=AdminCallback(action="user_info", user_id=user.telegram_id)
        )
    
    # Добавляем кнопки пагинации
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            ("⬅️ Назад", AdminCallback(action="prev_page", page=page-1, show_active=show_active))
        )
    
    if (page + 1) * per_page < len(users):
        pagination_buttons.append(
            ("Вперед ➡️", AdminCallback(action="next_page", page=page+1, show_active=show_active))
        )
    
    for text, callback_data in pagination_buttons:
        builder.button(text=text, callback_data=callback_data)
    
    # Кнопка возврата в главное меню управления пользователями
    builder.button(text="🔙 Назад", callback_data=AdminCallback(action="user_list"))
    
    # Регулируем расположение кнопок: список пользователей, затем пагинация в одной строке, затем кнопка "Назад"
    builder.adjust(1, len(pagination_buttons), 1)
    
    return builder.as_markup()

def get_admin_user_actions_menu(user_id: int, is_active: bool):
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✏️ Изменить данные", 
        callback_data=AdminCallback(action="edit_user_info", user_id=user_id)
    )
    builder.button(
        text="🔑 Изменить роль", 
        callback_data=AdminCallback(action="edit_role", user_id=user_id)
    )
    builder.button(
        text="💵 Изменить T-Point", 
        callback_data=AdminCallback(action="edit_t_points", user_id=user_id)
    )
    
    if is_active:
        builder.button(
            text="🚫 Деактивировать", 
            callback_data=AdminCallback(action="deactivate", user_id=user_id)
        )
    else:
        builder.button(
            text="✅ Активировать", 
            callback_data=AdminCallback(action="activate", user_id=user_id)
        )
    
    builder.button(text="🔙 Назад", callback_data=AdminCallback(action="user_list"))
    builder.adjust(1)
    return builder.as_markup()

def get_admin_edit_fields_menu(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Имя", callback_data=AdminCallback(action="edit_name", user_id=user_id))
    builder.button(text="👔 Должность", callback_data=AdminCallback(action="edit_position", user_id=user_id))
    builder.button(text="🏢 Отдел", callback_data=AdminCallback(action="edit_department", user_id=user_id))
    builder.button(text="📅 Дата найма", callback_data=AdminCallback(action="edit_hire_date", user_id=user_id))
    builder.button(text="🎂 Дата рождения", callback_data=AdminCallback(action="edit_birth_date", user_id=user_id))
    builder.button(text="🔑 Роль", callback_data=AdminCallback(action="edit_role", user_id=user_id))
    builder.button(text="💵 T-Point", callback_data=AdminCallback(action="edit_tpoint", user_id=user_id))
    builder.button(text="🔙 Назад", callback_data=AdminCallback(action="user_info", user_id=user_id))
    builder.adjust(2)
    return builder.as_markup()
