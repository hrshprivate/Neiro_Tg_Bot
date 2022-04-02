from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="О шифровании ℹ️"),
            KeyboardButton(text="Связь ✔️")
        ],
        [
            KeyboardButton(text="Сравнение фото 😵"),
            KeyboardButton(text="Анализ фото 🖤")
        ],
    ],
    resize_keyboard=True
)
