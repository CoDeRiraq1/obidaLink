import asyncio
import requests

from telegram.ext import Application
from config import TOKEN
from handlers.user_handlers import get_user_handlers
from handlers.admin_handlers import get_admin_handlers

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handlers(get_user_handlers())
    application.add_handlers(get_admin_handlers())
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
