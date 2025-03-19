from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Callable, Dict, Any, Awaitable

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
            
            # Проверяем членство в группе
            try:
                member = await bot.get_chat_member(self.target_group_id, user_id)
                # Если пользователь не является участником группы, отклоняем запрос
                if member.status in ["left", "kicked", "banned"]:
                    await event.answer("Вы должны быть участником группы для использования этого бота.")
                    return
            except Exception as e:
                await event.answer("Произошла ошибка при проверке членства в группе.")
                return
        
        # Если проверка пройдена, продолжаем обработку
        return await handler(event, data)