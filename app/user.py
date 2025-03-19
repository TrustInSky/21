from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

user_router = Router()


@user_router.message(CommandStart)
async def cmd_star(message: Message):
    await message.answer