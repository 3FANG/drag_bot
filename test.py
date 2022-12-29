from aiogram import Bot, Dispatcher, executor
from aiogram.types import ContentType, Message

TOKEN = '5170749920:AAEdfUIe2hzWx_rB0mrqMB3PghTErIKdXq8'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=ContentType.ANY)
async def start(message: Message):
    print(message)
    await message.answer(text='Принято')

if __name__ == '__main__':
    executor.start_polling(dp)
