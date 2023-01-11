from aiogram import Dispatcher
from aiogram.types import Message, ContentType


async def echo(message: Message):
    await message.answer(message)
    await message.delete()

def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(echo, content_types=ContentType.ANY)
