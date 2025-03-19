import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from app.user import user_router
from app.database.models import Base
from app.database.models import ansync_main



async def main():
    await ansync_main()
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    storage = MemoryStorage()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown) 
    dp.include_routers(user_router)
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
    
    
    
    