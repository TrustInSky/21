from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

user_router = Router()


@user_router.message(CommandStart)
async def cmd_start(message: Message):
    chat_id = message.chat.id
    
    await message.answer(f"ID этого чата/группы: {chat_id}")