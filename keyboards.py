from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# МЕНЮ АДМИНА  (ДОБАВЛЕНИЕ / УДАЛЕНИЕ / ОБНОВИТЬ)
admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Crime Case📂'),
         KeyboardButton(text='Контент🎬')],
        [],
        [KeyboardButton(text='Добавить➕')],
        [KeyboardButton(text='Отредактировать📝'),
         KeyboardButton(text='Удалить➖')]
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

go_back_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вернуться🔙")]
    ],
    resize_keyboard=True
)

# МЕНЮ ПОЛЬЗОВАТЕЛЯ
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🔍 Найти дело'),
         KeyboardButton(text='📖 История дня')],
        [KeyboardButton(text='📚 Что посмотреть'),
         KeyboardButton(text='⭐ Избранное')]
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

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отмена")]],
    resize_keyboard=True
)