from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os, hashlib
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "echo"
    link = f'https://emojipedia.org/search/?q={text}'
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id=result_id,
        title='emojipedia.org: ',
        url=link,
        input_message_content=types.InputTextMessageContent(message_text=link))]

    await query.answer(articles, cache_time=1, is_personal=True)

