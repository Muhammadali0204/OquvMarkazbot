from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kurslar(listt):
    kurs = InlineKeyboardMarkup(
        row_width=1
    )
    for kurs1 in listt:
        kurs.insert(InlineKeyboardButton(text=kurs1[1], callback_data=kurs1[0]))
        
    kurs.insert(InlineKeyboardButton(text="🔙Ortga", callback_data="back"))
    
    return kurs