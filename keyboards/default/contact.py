from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔢Raqamimni yuborish', request_contact=True)
        ],
    ], resize_keyboard=True
)


contact2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔢Raqamimni yuborish', request_contact=True)
        ],
        [
            KeyboardButton(text="◀️Ortga")
        ]
    ], resize_keyboard=True
)