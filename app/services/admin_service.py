from datetime import date
from typing import List, Optional
from app.services.profile_service import ProfileService
from app.database.models.user_model import User, UserRole
from app.repositories.user_repository import (
    get_user_by_telegram_id, get_all_users, 
    activate_user, deactivate_user, update_user
)

class AdminService:
    @staticmethod
    async def check_admin_access(telegram_id: int) -> bool:
        """Проверяет, есть ли у пользователя права администратора/HR"""
        user = await get_user_by_telegram_id(telegram_id)
        return user and user.can_manage_users()

    @staticmethod
    async def get_users_list(is_active: bool = True) -> List[User]:
        """Возвращает список активных/неактивных пользователей"""
        users = await get_all_users()
        return [user for user in users if user.is_active == is_active]

    @staticmethod
    async def change_user_status(user_id: int, activate: bool) -> bool:
        """Активирует/деактивирует пользователя"""
        if activate:
            return await activate_user(user_id)
        return await deactivate_user(user_id)

    @staticmethod
    async def update_user_field(user_id: int, field: str, value) -> bool:
        """Обновляет поле пользователя"""
        user = await get_user_by_telegram_id(user_id)
        if not user:
            return False
        
        setattr(user, field, value)
        return await update_user(user)
    
    @staticmethod
    async def get_user_info(user_id: int) -> Optional[dict]:
        """Возвращает информацию о пользователе в формате для отображения"""
        user = await get_user_by_telegram_id(user_id)
        if not user:
            return None
        
        experience_data = ProfileService.calculate_work_experience(user.hire_date)
        age_text = ProfileService.calculate_age(user.birth_date)
        
        return {
            "telegram_id": user.telegram_id,
            "username": user.username,
            "name": user.name,
            "birth_date": user.birth_date.strftime('%d.%m.%Y') if user.birth_date else None,
            "age_text": age_text,
            "hire_date": user.hire_date.strftime('%d.%m.%Y') if user.hire_date else None,
            "position": user.position,
            "department": user.department,
            "experience_text": experience_data["text"],
            "role": user.role.value,
            "is_active": user.is_active,
            "t_points": user.t_points
        }