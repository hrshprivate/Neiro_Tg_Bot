from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


class Photo(StatesGroup):
    password = State()
    photo = State()


class Decode(StatesGroup):
    photo_decode = State()


class Answer(StatesGroup):
    photo = State()
