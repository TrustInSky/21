from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from app.keyboards import get_main_menu, get_profile_menu
from app.callbacks import ProfileCallback

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите опцию:",
        reply_markup=get_main_menu()
    )

@user_router.callback_query(ProfileCallback.filter(F.action == "profile"))
async def show_profile(callback: CallbackQuery, callback_data: ProfileCallback):
    # Заглушка для БД
    user_info = f"Имя: {callback.from_user.first_name}\nUsername:@{callback.from_user.username}\n"
    
    await callback.message.edit_text(
        f"Ваш профиль:\n{user_info}",
        reply_markup=get_profile_menu()
    )
    await callback.answer()

@user_router.callback_query(ProfileCallback.filter(F.action == "back"))
async def back_to_menu(callback: CallbackQuery, callback_data: ProfileCallback):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

@user_router.callback_query(ProfileCallback.filter(F.action == "edit"))
async def edit_profile(callback: CallbackQuery, callback_data: ProfileCallback):
    await callback.answer("Редактирование профиля (заглушка)")