from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command

from loader import bot, dp
from states.test import Test
from utils.db_api.sqlite import add_command
from utils.misc.main import compare_faces


@dp.message_handler(Command("test"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Сравнение фотографий.\n"
                         "Заявленная точность 95%+. \n\n"
                         "Загружайте фото для сравнения!")
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
    # answer = message.text

    # Ваирант 2 получения state
    # state = dp.current_state(chat=message.chat.id, user=message.from_user.id)

    # Вариант 1 сохранения переменных - записываем через key=var
    # await state.update_data(answer1=answer)

    # # Вариант 2 - передаем как словарь
    # await state.update_data(
    #     {"answer1": answer}
    # )

    # Вариант 3 - через state.proxy
    async with state.proxy() as data:
        data["Q1"] = message.photo[0].file_id
    await message.answer("Загружаем новое фото")
    await Test.next()


@dp.message_handler(content_types=['photo'], state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    # answer = message.text

    # Ваирант 2 получения state
    # state = dp.current_state(chat=message.chat.id, user=message.from_user.id)

    # Вариант 1 сохранения переменных - записываем через key=var
    # await state.update_data(answer1=answer)

    # # Вариант 2 - передаем как словарь
    # await state.update_data(
    #     {"answer1": answer}
    # )
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

