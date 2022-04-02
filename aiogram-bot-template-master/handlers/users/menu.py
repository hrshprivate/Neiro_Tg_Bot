import io

from aiogram import types
from aiogram.dispatcher import FSMContext
from translate import Translator

from loader import dp, bot
from aiogram.types import Message, ReplyKeyboardMarkup
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text

from states.test import Test, Answer
from utils.db_api.sqlite import add_command
from utils.misc.main import compare_faces, ff


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выбери из меню", reply_markup=menu)


@dp.message_handler(Text(equals=["О шифровании ℹ️"]))
async def get_item(message: Message):

    await message.answer(f"Необходимые рекомендации: ⬇️\n"
                         f"1️⃣ Шифрование работает для фотографий .jpg формата,  \n"
                         f"2️⃣ Фотографию сжимать не надо, отправляем документом, \n"
                         f"3️⃣ Бот может расшифровать только то, что зашифровал, \n"
                         f"🔥 /items - Запуск шифрования", reply_markup=ReplyKeyboardMarkup())


@dp.message_handler(Text(equals=["Связь ✔️"]))
async def get_answer(message: Message):
    await message.answer(f"Для связи с автором бота необходимо пройти проверку, "
                         f"Перейдите для выполнения теста: /connect", reply_markup=ReplyKeyboardMarkup())


@dp.message_handler(Text(equals=["Сравнение фото 😵"]), state=None)
async def get_answer(message: Message):
    await message.answer("Сравнение фотографий.\n"
                         "Заявленная точность 95%+. \n\n"
                         "Загружайте фото лиц для сравнения!")
    await Test.Q1.set()


@dp.message_handler(Command("cancel"), state="*")
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_data(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


@dp.message_handler(content_types=['photo'], state=Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Q1"] = message.photo[0].file_id
    await message.answer("Загружаем новое фото")
    await Test.next()


@dp.message_handler(content_types=['photo'], state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer_1 = await bot.get_file(data.get("Q1"))
    downloaded_file_first = await bot.download_file(answer_1.file_path)
    async with state.proxy() as data:
        data["Q2"] = message.photo[0].file_id
    answer_2 = await bot.get_file(message.photo[0].file_id)
    downloaded_file_second = await bot.download_file(answer_2.file_path)
    result = compare_faces(downloaded_file_first, downloaded_file_second)
    await message.answer(f'Результат сравнения равен - {result}')
    await add_command(state)
    await state.finish()

#######################################################################


@dp.message_handler(Text(equals=["Анализ фото 🖤"]), state=None)
async def get_answer(message: Message):
    await message.answer("Получение информации о фото.\n"
                         "Терпение и получим результат. \n\n"
                         "Загружайте фото лица для обработки!\n"
                         "Фото должно быть в хорошем качестве, определяет только одно лицо!\n"
                         "Отправляем документом(без сжатия)")
    await Answer.photo.set()


@dp.message_handler(content_types=['document'], state=Answer.photo)
async def answer_q1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.document.file_id
    photo_name = message.document.file_id
    downloaded_file = await bot.download_file_by_id(photo_name)
    file = "123.jpg"
    with open(file, "wb") as f:
        f.write(downloaded_file.read())
    result = ff(file)

    translator = Translator(to_lang="Russian")
    await message.answer(f"Получаем полную инфу: \n"
                         f"Примерный возраст - {result['age']} \n"
                         f"Примерная раса - {translator.translate(result['dominant_race'])} \n"
                         f"Примерный пол - {translator.translate(result['gender'])} \n"
                         f"Примерная эмоция - {translator.translate(result['dominant_emotion'])} \n")
    await state.finish()






# @dp.message_handler(Text(equals=["О шифровании ℹ️", "Анализ фото", "Поиск по лицу"]))




