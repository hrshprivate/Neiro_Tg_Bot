import io
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from stegano.exifHeader import exifHeader
import requests


from keyboards.inline.callback_date import buy_callback, test_callback
from keyboards.inline.choice_buttons import choice, adm, pear
from loader import dp, bot
from states.test import Photo, Decode, Answer


@dp.message_handler(Command("items"), state=None)
async def show_items(message: Message):
    await message.answer(text="Выбирай. \n"
                              "Жмите отмена, если ничего не надо", reply_markup=choice)


@dp.callback_query_handler(buy_callback.filter(name="code"), state=None)
async def start(call: CallbackQuery):
    await call.answer("Сначала пароль!", show_alert=True)
    await Photo.password.set()


@dp.callback_query_handler(text="cancel", state="*")
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer(f"Вы нажали кнопку отменить", show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()


@dp.callback_query_handler(buy_callback.filter(name="code"))
@dp.message_handler(state=Photo.password)
async def password(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text
    await message.answer("Добавляем фото без сжатия!")
    await Photo.next()


@dp.callback_query_handler(buy_callback.filter(name="code"))
@dp.message_handler(content_types=['document'], state=Photo.photo)
async def photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.document.file_id
    password_one = await state.get_data()
    password_value = password_one.get('password')
    document = message.document.file_id
    downloaded_file = await bot.download_file_by_id(document)
    exifHeader.hide(downloaded_file, "2.jpg", str(password_value))
    with open("2.jpg", "rb") as f:
        file1337 = f.read()
    file = io.BytesIO(file1337)
    file.name = "result.jpg"
    await bot.send_document(chat_id=message.chat.id, document=file)
    await state.finish()


@dp.callback_query_handler(buy_callback.filter(name="decode"), state=None)
async def decoding(call: CallbackQuery, callback_data: dict):
    # await call.answer(cache_time=60)
    await call.message.answer("Загружайте Ваше фото без сжатия!")
    await Decode.photo_decode.set()


@dp.callback_query_handler(buy_callback.filter(name="decode"))
@dp.message_handler(content_types=['document'], state=Decode.photo_decode)
async def photo_decoding(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo_decode"] = message.document.file_id
    photo = message.document.file_id
    downloaded_file = await bot.download_file_by_id(photo)
    file = io.BytesIO(downloaded_file.getvalue())
    result = exifHeader.reveal(file)
    await message.answer(f"Получай свой текст: \n"
                         f"{result.decode()}")
    await state.finish()


@dp.message_handler(Command("connect"))
async def show_items(message: Message):
    await message.answer(text="При готовности нажать кнопку готов.  ", reply_markup=adm)


@dp.callback_query_handler(test_callback.filter(name="checker"), state=None)
async def start1337(call: CallbackQuery):
    await call.answer(cache_time=60)
    await bot.send_photo(chat_id=call.message.chat.id,
                         photo=open("1.jpg", "rb"),
                         caption="Сколько цветов у квадрата?, "
                                 "Укажите цифру. ")
    await Answer.photo.set()


@dp.callback_query_handler(test_callback.filter(name="checker"))
@dp.message_handler(content_types=['text'], state=Answer.photo)
async def testing(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = int(message.text)
    data = await state.get_data()
    value = data.get('photo')
    if value == 16:
        await message.answer("Ссылку получай", reply_markup=pear)
        await state.finish()
    else:
        await message.answer("Ответ неверен, попробуйте позже!")
        await state.finish()
