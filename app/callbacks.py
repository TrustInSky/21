from aiogram.filters.callback_data import CallbackData


class AdminCallback(CallbackData, prefix="admin"):
    action: str
    user_id: int = 0 
    
class HrCallback(CallbackData,prefix="hr"):
    action: str
    user_id: int | None = None 
    
    
class ProfileCallback(CallbackData, prefix="profile"):
    action: str