from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Foydalanuvchilar soni'),
            KeyboardButton(text='Reklama')
        ],
        [
            KeyboardButton(text="Kurs qo'shish"),
            KeyboardButton(text="Kursni o'chirish")
        ],
        [
            KeyboardButton(text="Kursni tahrirlash"),
            KeyboardButton(text="Chegirmalarni o'zgartirish"),
        ],
        [
            KeyboardButton(text="Menu"),
        ]
    ], resize_keyboard=True
)