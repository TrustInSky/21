from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.models.user_model import User
from app.callbacks import HrCallback, AdminCallback

def get_user_list_markup(users, page=0, page_size=20, show_active=True, callback_type="admin"):
    builder = InlineKeyboardBuilder()
    
    filtered_users = [u for u in users if u.is_active == show_active]
    start = page * page_size
    end = min(start + page_size, len(filtered_users))
    
    for user in filtered_users[start:end]:
        name = user.name if user.name else f"@{user.username}" if user.username else f"ID: {user.telegram_id}"
        position = f" | {user.position}" if user.position else ""
        department = f" | {user.department}" if user.department else ""
        
        display_text = f"{name}{position}{department}"
        if len(display_text) > 90:  
            display_text = display_text[:57] + "..."
        
        callback_data = (
            AdminCallback(action="user_info", user_id=user.telegram_id) if callback_type == "admin"
            else HrCallback(action="user_info", user_id=user.telegram_id)
        )
        
        builder.button(text=display_text, callback_data=callback_data)
    
    pagination_callback = (
        AdminCallback(action="prev_page", user_id=page) if callback_type == "admin"
        else HrCallback(action="prev_page", user_id=page)
    )
    
    if page > 0:
        builder.button(text="⬅️", callback_data=pagination_callback)
    
    if end < len(filtered_users):
        builder.button(text="➡️", callback_data=pagination_callback)
    
    back_callback = (
        AdminCallback(action="user_list") if callback_type == "admin"
        else HrCallback(action="user_list")
    )
    builder.button(text="🔙 Назад", callback_data=back_callback)
    
    builder.adjust(2, 1, 1)
    return builder.as_markup()