from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards.user_keyboards import get_main_menu, get_profile_menu, get_profile_edit_menu
from app.callbacks import ProfileCallback
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from datetime import datetime, date

user_router = Router()

class ProfileStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_birth_date = State()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    user = await UserService.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )
    
    welcome_text = "Добро пожаловать!" if not user.is_active else "Добро пожаловать обратно!"
    await message.answer(
        f"{welcome_text} Выберите опцию:",
        reply_markup=get_main_menu(user)
    )

@user_router.callback_query(ProfileCallback.filter(F.action == "profile"))
async def show_profile(callback: CallbackQuery, callback_data: ProfileCallback):
    user = await UserService.get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username
    )
    
    if not user.is_active:
        await callback.answer("Ваша учетная запись неактивна. Обратитесь к HR или администратору.", show_alert=True)
        return
    
    experience_data = ProfileService.calculate_work_experience(user.hire_date)
    age_text = ProfileService.calculate_age(user.birth_date)
    profile_text = ProfileService.format_profile_text(user, experience_data["text"], age_text)
    
    await callback.message.edit_text(
        profile_text,
        reply_markup=get_profile_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

@user_router.callback_query(ProfileCallback.filter(F.action == "back"))
async def back_to_menu(callback: CallbackQuery, callback_data: ProfileCallback):
    user = await UserService.get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username
    )
    
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu(user)
    )
    await callback.answer()

@user_router.callback_query(ProfileCallback.filter(F.action == "edit"))
async def edit_profile(callback: CallbackQuery, callback_data: ProfileCallback):
    user = await UserService.get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username
    )
    
    if not user.is_active:
        await callback.answer("Ваша учетная запись неактивна. Обратитесь к HR или администратору.", show_alert=True)
        return
    
    await callback.message.edit_text(
        text="Выберите, что хотите изменить:",
        reply_markup=get_profile_edit_menu()
    )
    await callback.answer()

@user_router.callback_query(ProfileCallback.filter(F.action == "edit_name"))
async def edit_name(callback: CallbackQuery, callback_data: ProfileCallback, state: FSMContext):
    await callback.message.edit_text("Введите ваше новое имя:")
    await state.set_state(ProfileStates.waiting_for_name)
    await callback.answer()

@user_router.message(ProfileStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    new_name = message.text.strip()
    
    if not new_name:
        await message.answer("Имя не может быть пустым. Введите снова:")
        return
    
    user = await UserService.update_user_name(message.from_user.id, new_name)
    if not user:
        await message.answer("Пользователь не найден.")
        await state.clear()
        return
    
    await message.answer(
        f"✅ Имя успешно обновлено на <b>{new_name}</b>", 
        parse_mode="HTML"
    )
    await message.answer(
        "Выберите следующее действие:", 
        reply_markup=get_profile_menu()
    )
    await state.clear()

@user_router.callback_query(ProfileCallback.filter(F.action == "edit_birth_date"))
async def edit_birth_date(callback: CallbackQuery, callback_data: ProfileCallback, state: FSMContext):
    await callback.message.edit_text("Введите дату рождения в формате ДД.ММ.ГГГГ:")
    await state.set_state(ProfileStates.waiting_for_birth_date)
    await callback.answer()

@user_router.message(ProfileStates.waiting_for_birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    date_text = message.text.strip()
    
    try:
        birth_date = datetime.strptime(date_text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer("❌ Неверный формат даты. Введите снова в формате ДД.ММ.ГГГГ:")
        return
    
    if birth_date > date.today():
        await message.answer("Дата рождения не может быть в будущем!")
        return
    
    if birth_date.year < 1900:
        await message.answer("Укажите реальную дату рождения.")
        return
    
    user = await UserService.update_user_birth_date(message.from_user.id, birth_date)
    if not user:
        await message.answer("Пользователь не найден.")
        await state.clear()
        return
    
    await message.answer(
        f"✅ Дата рождения успешно обновлена на <b>{birth_date.strftime('%d.%m.%Y')}</b>", 
        parse_mode="HTML"
    )
    await message.answer(
        "Выберите следующее действие:", 
        reply_markup=get_profile_menu()
    )
    await state.clear()