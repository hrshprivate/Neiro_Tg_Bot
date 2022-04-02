from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_date import buy_callback, test_callback

choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=
[

    [
        InlineKeyboardButton(
            text="Шифрование ⌛",
            callback_data=buy_callback.new(name="code")
        ),
        InlineKeyboardButton(
            text="Расшифровка 💣",
            callback_data="buy:decode"
        )
    ],
    [
        InlineKeyboardButton(
            text="Отмена ❌",
            callback_data="cancel"
        )
    ]

]
                              )
adm = InlineKeyboardMarkup(row_width=2, inline_keyboard=
[

    [
        InlineKeyboardButton(
            text="Готов ❓ ",
            callback_data=test_callback.new(name="checker")
        ),
        InlineKeyboardButton(
            text="Отмена ❌",
            callback_data="cancel"
        )
    ],

]
                           )

pear = InlineKeyboardMarkup()

PEAR_LINK = "https://t.me/horsh1337"

pear_link = InlineKeyboardButton(text="Автор тут 🤜 ", url=PEAR_LINK)

pear.insert(pear_link)
