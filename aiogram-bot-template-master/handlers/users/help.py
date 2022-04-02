from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начало работы",
            "/help - Помощь",
            "/menu - Текстовые клавиатура",
            "/test - face recognition")
    
    await message.answer("\n".join(text))
