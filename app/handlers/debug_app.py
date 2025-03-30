import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.callbacks import AdminCallback

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем отдельный роутер для отладки
debug_router = Router()

# Этот обработчик поймает все callback-запросы с префиксом "admin"
@debug_router.callback_query(F.data.startswith("admin"))
async def debug_all_admin_callbacks(callback: CallbackQuery):
    logger.info(f"Получен callback: {callback.data}")
    # Не отвечаем на callback, чтобы не мешать основным обработчикам
    # но логируем его для отладки
    
# Добавляем обработчик, который будет ловить вообще все callback-запросы
@debug_router.callback_query()
async def debug_all_callbacks(callback: CallbackQuery):
    logger.info(f"Получен любой callback: {callback.data}")