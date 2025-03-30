from datetime import date, datetime
from app.database.models.user_model import User, UserRole
from app.repositories.user_repository import (
    get_user_by_telegram_id, create_user, 
    update_user, activate_user
)

class UserService:
    @staticmethod
    async def get_or_create_user(telegram_id: int, username: str) -> User:
        user = await get_user_by_telegram_id(telegram_id)
        
        if user:
            if not user.is_active:
                await activate_user(telegram_id)
            
            if user.username != username:
                user.username = username
                await update_user(user)
        else:
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                hire_date=date.today(),
                role=UserRole.USER,
                is_active=True
            )
            await create_user(new_user)
            user = new_user
        
        return user

    @staticmethod
    async def update_user_name(telegram_id: int, new_name: str) -> User:
        user = await get_user_by_telegram_id(telegram_id)
        if not user:
            return None
        
        user.name = new_name
        await update_user(user)
        return user

    @staticmethod
    async def update_user_birth_date(telegram_id: int, birth_date: date) -> User:
        user = await get_user_by_telegram_id(telegram_id)
        if not user:
            return None
        
        user.birth_date = birth_date
        await update_user(user)
        return user