import asyncio

from loguru import logger
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config.config import load_config, Config
from bot.handlers import register_all_handlers
import bot.database

async def main():
    logger.info('Bot started...')
    config: Config = load_config()

    bot: Bot = Bot(token=(config.tg_bot.token), parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

    register_all_handlers(dp)
    try:
        await dp.skip_updates()
        await dp.start_polling()
    finally:
        await bot.close()

def start_bot():
    try:
        asyncio.run(main())
    except Exception as ex:
        logger.error(ex)
