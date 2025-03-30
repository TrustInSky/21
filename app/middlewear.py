from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Dict, Any, Awaitable
from app.repositories.user_repository import get_user_by_telegram_id, deactivate_user

class GroupMembershipMiddleware(BaseMiddleware):
    def __init__(self, target_group_id: int):
        self.target_group_id = target_group_id
        super().__init__()
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Проверяем что это сообщение
        if isinstance(event, Message):
            user_id = event.from_user.id
            bot = data["bot"]
            
            # Проверяем наличие пользователя в базе
            user = await get_user_by_telegram_id(user_id)
            
            if user:
                # Проверяем членство в группе
                try:
                    member = await bot.get_chat_member(self.target_group_id, user_id)
                    
                    # Если пользователь не является участником группы, деактивируем его
                    if member.status in ["left", "kicked", "banned"]:
                        if user.is_active:
                            await deactivate_user(user_id)
                            await event.answer("Вы не являетесь участником группы. Ваш аккаунт деактивирован.")
                            return
                except Exception as e:
                    # Если произошла ошибка при проверке, продолжаем обработку
                    # но можно добавить логирование ошибки
                    pass
            
            # Если проверка пройдена или пользователя нет в базе, продолжаем обработку
        return await handler(event, data)