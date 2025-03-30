from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import date
from app.callbacks import AdminCallback
from app.keyboards.admin_keyboards import (
    get_admin_user_management_menu,
    get_admin_user_actions_menu,
    get_admin_edit_fields_menu,
    get_user_list_markup
)
from app.services.admin_service import AdminService
from app.services.user_list_service import UserListService
from app.services.profile_service import ProfileService
from app.database.models.user_model import UserRole

admin_router = Router()

class AdminEditStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_position = State()
    waiting_for_department = State()
    waiting_for_hire_date = State()
    waiting_for_birth_date = State()
    waiting_for_role = State()
    waiting_for_t_points = State()

# Основные команды управления пользователями
@admin_router.callback_query(AdminCallback.filter(F.action == "user_list"))
async def show_user_management(callback: CallbackQuery, callback_data: AdminCallback):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции", show_alert=True)
        return
    
    await callback.message.edit_text(
        "Управление сотрудниками:",
        reply_markup=get_admin_user_management_menu()
    )
    await callback.answer()

@admin_router.callback_query(AdminCallback.filter(F.action == "active_users"))
async def show_active_users(callback: CallbackQuery, callback_data: AdminCallback):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции", show_alert=True)
        return
    
    active_users = await UserListService.get_active_users()
    
    if not active_users:
        await callback.message.edit_text(
            "Нет активных пользователей.",
            reply_markup=get_admin_user_management_menu()
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "Активные сотрудники:",
        reply_markup=get_user_list_markup(active_users, show_active=True)
    )
    await callback.answer()

@admin_router.callback_query(AdminCallback.filter(F.action == "inactive_users"))
async def show_inactive_users(callback: CallbackQuery, callback_data: AdminCallback):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции", show_alert=True)
        return
    
    inactive_users = await UserListService.get_inactive_users()
    
    if not inactive_users:
        await callback.message.edit_text(
            "Нет неактивных пользователей.",
            reply_markup=get_admin_user_management_menu()
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "Неактивные сотрудники:",
        reply_markup=get_user_list_markup(inactive_users, show_active=False)
    )
    await callback.answer()

# Просмотр и редактирование профиля пользователя
@admin_router.callback_query(AdminCallback.filter(F.action == "user_info"))
async def show_user_info(callback: CallbackQuery, callback_data: AdminCallback):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции", show_alert=True)
        return
    
    user_info = await AdminService.get_user_info(callback_data.user_id)
    if not user_info:
        await callback.answer("Пользователь не найден", show_alert=True)
        return
    
    info_text = ProfileService.format_admin_profile_text(user_info)
    
    await callback.message.edit_text(
        info_text,
        reply_markup=get_admin_user_actions_menu(callback_data.user_id, user_info['is_active']),
        parse_mode="HTML"
    )
    await callback.answer()

@admin_router.callback_query(AdminCallback.filter(F.action == "edit_user_info"))
async def edit_user_start(callback: CallbackQuery, callback_data: AdminCallback):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции", show_alert=True)
        return
    
    user_info = await AdminService.get_user_info(callback_data.user_id)
    if not user_info:
        await callback.answer("Пользователь не найден", show_alert=True)
        return
    
    await callback.message.edit_text(
        f"Редактирование: @{user_info['username'] or 'Без имени'}",
        reply_markup=get_admin_edit_fields_menu(callback_data.user_id)
    )
    await callback.answer()

# Управление статусом пользователя
@admin_router.callback_query(AdminCallback.filter(F.action == "deactivate"))
async def deactivate_user_handler(callback: CallbackQuery, callback_data: AdminCallback):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции", show_alert=True)
        return
    
    success = await AdminService.change_user_status(callback_data.user_id, False)
    if success:
        await callback.answer("Пользователь деактивирован", show_alert=True)
        await show_user_info(callback, callback_data)
    else:
        await callback.answer("Ошибка при деактивации", show_alert=True)

@admin_router.callback_query(AdminCallback.filter(F.action == "activate"))
async def activate_user_handler(callback: CallbackQuery, callback_data: AdminCallback):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа к этой функции", show_alert=True)
        return
    
    success = await AdminService.change_user_status(callback_data.user_id, True)
    if success:
        await callback.answer("Пользователь активирован", show_alert=True)
        await show_user_info(callback, callback_data)
    else:
        await callback.answer("Ошибка при активации", show_alert=True)

# Редактирование полей пользователя
@admin_router.callback_query(AdminCallback.filter(F.action == "edit_name"))
async def edit_user_name_start(callback: CallbackQuery, callback_data: AdminCallback, state: FSMContext):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа", show_alert=True)
        return
    
    await state.update_data(user_id=callback_data.user_id)
    user_info = await AdminService.get_user_info(callback_data.user_id)
    
    await callback.message.edit_text(
        f"Текущее имя: {user_info['name'] or 'Не указано'}\n"
        "Введите новое имя:"
    )
    await state.set_state(AdminEditStates.waiting_for_name)
    await callback.answer()

@admin_router.message(AdminEditStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    success = await AdminService.update_user_field(
        data['user_id'], 
        'name', 
        message.text.strip()
    )
    
    if success:
        await message.answer("Имя успешно обновлено")
        await show_user_info_after_edit(message, data['user_id'])
    else:
        await message.answer("Ошибка обновления")
    
    await state.clear()

# Аналогичные хендлеры для других полей (position, department и т.д.)
# Шаблон аналогичен edit_user_name_start/process_name

@admin_router.callback_query(AdminCallback.filter(F.action == "edit_role"))
async def edit_role_start(callback: CallbackQuery, callback_data: AdminCallback, state: FSMContext):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа", show_alert=True)
        return
    
    await state.update_data(user_id=callback_data.user_id)
    user_info = await AdminService.get_user_info(callback_data.user_id)
    
    roles = "\n".join([f"- {role.value}" for role in UserRole])
    await callback.message.edit_text(
        f"Текущая роль: {user_info['role']}\n"
        f"Доступные роли:\n{roles}\n"
        "Введите новую роль:"
    )
    await state.set_state(AdminEditStates.waiting_for_role)
    await callback.answer()

@admin_router.message(AdminEditStates.waiting_for_role)
async def process_role(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        role = UserRole(message.text.strip().lower())
        success = await AdminService.update_user_field(
            data['user_id'], 
            'role', 
            role
        )
        
        if success:
            await message.answer("Роль успешно обновлена")
            await show_user_info_after_edit(message, data['user_id'])
        else:
            await message.answer("Ошибка обновления")
    except ValueError:
        await message.answer("Некорректная роль. Введите одну из доступных.")
        return
    
    await state.clear()

@admin_router.callback_query(AdminCallback.filter(F.action == "edit_t_points"))
async def edit_t_points_start(callback: CallbackQuery, callback_data: AdminCallback, state: FSMContext):
    if not await AdminService.check_admin_access(callback.from_user.id):
        await callback.answer("У вас нет доступа", show_alert=True)
        return
    
    await state.update_data(user_id=callback_data.user_id)
    user_info = await AdminService.get_user_info(callback_data.user_id)
    
    await callback.message.edit_text(
        f"Текущие T-Points: {user_info['t_points']}\n"
        "Введите новое значение:"
    )
    await state.set_state(AdminEditStates.waiting_for_t_points)
    await callback.answer()

@admin_router.message(AdminEditStates.waiting_for_t_points)
async def process_t_points(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        t_points = int(message.text.strip())
        success = await AdminService.update_user_field(
            data['user_id'], 
            't_points', 
            t_points
        )
        
        if success:
            await message.answer("T-Points успешно обновлены")
            await show_user_info_after_edit(message, data['user_id'])
        else:
            await message.answer("Ошибка обновления")
    except ValueError:
        await message.answer("Введите целое число")
        return
    
    await state.clear()

# Вспомогательные функции
async def show_user_info_after_edit(message: Message, user_id: int):
    """Показывает обновленную информацию о пользователе после редактирования"""
    user_info = await AdminService.get_user_info(user_id)
    if not user_info:
        await message.answer("Ошибка: пользователь не найден")
        return
    
    info_text = ProfileService.format_admin_profile_text(user_info)
    await message.answer(
        info_text,
        reply_markup=get_admin_user_actions_menu(user_id, user_info['is_active']),
        parse_mode="HTML"
    )