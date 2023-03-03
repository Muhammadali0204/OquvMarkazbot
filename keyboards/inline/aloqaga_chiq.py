from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def aloqa_keyboard(id):
    keyboard_aloqa = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Raqam ushbu foydalanuvchiga tegishli emas❌", callback_data=f"wrong_number:{id}")
            ],
            [
                InlineKeyboardButton(text="Bajarildi ✅", callback_data="ok")
            ]
        ]
    )
    return keyboard_aloqa