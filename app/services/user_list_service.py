from typing import List, Dict, Any, Optional
from app.database.models.user_model import User
from app.repositories.user_repository import get_all_users
from app.services.profile_service import ProfileService

class UserListService:
    @staticmethod
    async def get_all_users_formatted() -> List[Dict[str, Any]]:
        """Retrieves all users and formats them for display"""
        users = await get_all_users()
        
        formatted_users = []
        for user in users:
            # Calculate additional fields needed for display
            experience_info = ProfileService.calculate_work_experience(user.hire_date)
            age_text = ProfileService.calculate_age(user.birth_date)
            
            # Create a formatted user dict
            formatted_user = {
                'telegram_id': user.telegram_id,
                'username': user.username,
                'name': user.name,
                'birth_date': user.birth_date.strftime('%d.%m.%Y') if user.birth_date else None,
                'hire_date': user.hire_date.strftime('%d.%m.%Y') if user.hire_date else None,
                'position': user.position,
                'department': user.department,
                'role': user.role.value,
                'is_active': user.is_active,
                't_points': user.t_points,
                'experience_text': experience_info['text'],
                'age_text': age_text
            }
            formatted_users.append(formatted_user)
            
        return formatted_users
    
    @staticmethod
    async def get_active_users() -> List[Dict[str, Any]]:
        """Retrieves only active users and formats them"""
        all_users = await UserListService.get_all_users_formatted()
        return [user for user in all_users if user['is_active']]
    
    @staticmethod
    async def get_inactive_users() -> List[Dict[str, Any]]:
        """Retrieves only inactive users and formats them"""
        all_users = await UserListService.get_all_users_formatted()
        return [user for user in all_users if not user['is_active']]
    
    @staticmethod
    def get_paginated_users(users: List[Dict[str, Any]], page: int, per_page: int = 10) -> List[Dict[str, Any]]:
        """Returns a paginated list of users"""
        start = (page - 1) * per_page  # Start from 0 for page 1
        end = start + per_page
        return users[start:end]
    
    @staticmethod
    def format_user_list_item(user: Dict[str, Any]) -> str:
        """Formats a single user for display in the list"""
        status = '✅ Активен' if user['is_active'] else '❌ Неактивен'
        return (f"👤 <b>{user['name'] or 'Без имени'}</b>\n"
                f"🏢 {user['department'] or 'Без отдела'} | 👔 {user['position'] or 'Без должности'}\n"
                f"🔄 {status}\n")
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a specific user by ID"""
        all_users = await UserListService.get_all_users_formatted()
        for user in all_users:
            if user['telegram_id'] == user_id:
                return user
        return None