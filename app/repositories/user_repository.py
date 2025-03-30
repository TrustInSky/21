from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from app.database.models.user_model import User, UserModel, UserRole
from app.database.connection import async_session
from datetime import date

# Получить пользователя по telegram_id
async def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    async with async_session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        user_model = result.scalar_one_or_none()
        
        if user_model:
            return user_model.to_entity()
        return None

# Создать нового пользователя
async def create_user(user: User) -> int:
    async with async_session() as session:
        user_model = user.to_model()
        session.add(user_model)
        await session.commit()
        await session.refresh(user_model)
        return user_model.id

# Обновить пользователя
async def update_user(user: User) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.telegram_id == user.telegram_id)
        )
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            return False
        
        user_model.username = user.username
        user_model.name = user.name
        user_model.hire_date = user.hire_date
        user_model.birth_date = user.birth_date
        user_model.work_experience = user.work_experience
        user_model.position = user.position
        user_model.department = user.department
        user_model.role = user.role.value
        user_model.is_active = user.is_active
        user_model.t_points = user.t_points
        
        await session.commit()
        return True

# Деактивировать пользователя
async def deactivate_user(telegram_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        user_model = result.scalar_one_or_none()

        if not user_model:
            return False
        
        user_model.is_active = False
        await session.commit()
        return True

# Активировать пользователя
async def activate_user(telegram_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        user_model = result.scalar_one_or_none()

        if not user_model:
            return False
        
        user_model.is_active = True
        await session.commit()
        return True

# Получить всех активных пользователей
async def get_all_active_users() -> List[User]:
    async with async_session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.is_active == True)
        )
        user_models = result.scalars().all()
        return [user_model.to_entity() for user_model in user_models]

# Получить всех пользователей (активных и нет)
async def get_all_users() -> List[User]:
    async with async_session() as session:
        result = await session.execute(select(UserModel))
        user_models = result.scalars().all()
        return [user_model.to_entity() for user_model in user_models]
