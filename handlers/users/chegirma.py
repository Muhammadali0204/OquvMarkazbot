from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from data.config import ADMINS


from loader import dp, db, bot


@dp.message_handler(text="🎁Chegirmalar")
async def chegirma(msg : types.Message):
    chegirma = db.select_user(1)
    if chegirma[2] == None:
        await msg.answer("<b>Chegirmalar mavjud emas!</b>")
    else:
        try:
            await msg.answer(chegirma[2])
        except :
            await msg.answer("<b>Chegirmalar mavjud emas!</b>")
    