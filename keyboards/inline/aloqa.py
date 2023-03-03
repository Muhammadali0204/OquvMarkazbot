from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def aloqa(call):
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📱Aloqaga chiqish", callback_data=call)
        ]
    ]
    
)
    return keyboard