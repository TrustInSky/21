import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from app.handlers.user import user_router
from app.handlers.admin import admin_router
from app.handlers.debug_app import debug_router
from app.database.models.user_model import Base
from app.database.connection import init_db
from app.middlewear import GroupMembershipMiddleware



async def main():
    await init_db()
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    storage = MemoryStorage()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown) 
    dp.message.middleware(GroupMembershipMiddleware(target_group_id=os.getenv("GROUP_ID")))
    dp.include_routers(user_router,debug_router,admin_router)
    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):
    print('✅ Бот запущен')
    print("База данных инициализирована")

async def shutdown(dispatcher: Dispatcher):
    print('❌ Бот остановлен')





if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    
    
    
    