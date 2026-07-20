from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# МЕНЮ АДМИНА  (ДОБАВЛЕНИЕ / УДАЛЕНИЕ / ОБНОВИТЬ)
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='добавить')],
        [KeyboardButton(text='отредактировать'),
         KeyboardButton(text='удалить')]
    ],
    resize_keyboard=True,
    input_field_placeholder='tup button'
)

append_catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Crime Case", callback_data='crime_сase'),
            InlineKeyboardButton(text="Контент", callback_data='crime_content'),
        ]
    ]
)

delete_catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Crime Case", callback_data='delete_сase'),
            InlineKeyboardButton(text="Контент", callback_data='delete_content'),
        ]
    ]
)

update_catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Crime Case", callback_data='update_сase'),
            InlineKeyboardButton(text="Контент", callback_data='update_content'),
        ]
    ]
)


# МЕНЮ ПОЛЬЗОВАТЕЛЯ
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='menu')],
        [KeyboardButton(text='back'),
         KeyboardButton(text='contacts')]
    ],
    resize_keyboard=True,
    input_field_placeholder='tup button'
)

catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Go to Bot", url="https://t.me/fontspay_bot"),
            InlineKeyboardButton(text="Back", callback_data='crime_back'),
        ]
    ]
)