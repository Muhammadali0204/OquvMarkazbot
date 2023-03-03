from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from data.config import ADMINS


from loader import dp, db, bot, temp


@dp.message_handler(text="Chegirmalarni o'zgartirish", chat_id = ADMINS)
async def chegirmalar(msg : types.Message, state : FSMContext):
    chegirma = db.select_user(1)
    if chegirma[2] != None:
        await msg.answer("<b>Hozirgi chegirmalar bo'limi uchun post : </b>")
        try:
            await msg.answer(chegirma[2])
        except Exception as e:
            await msg.answer(f"<b>Xatolik yuz berdi : \n(Yangi post yuboravering)</b>{e}")
        await msg.answer("<b>O'zgartirmoqchi bo'lgan postni yuboring : </b>", reply_markup=bekor)
        await state.set_state("chegirma_uzgarishi")
    else:
        await msg.answer("<b>Chegirmalar uchun post mavjud emas, qo'shish uchun post yuboring!</b>", reply_markup=bekor)
        await state.set_state("chegirma_uzgarishi")
        
@dp.message_handler(state="chegirma_uzgarishi", text="◀️Ortga")
async def ortga(msg : types.Message, state : FSMContext):
    await msg.answer("<i>Menu : </i>", reply_markup=admin)
    await state.finish()
    
@dp.message_handler(state="chegirma_uzgarishi")
async def uzgarish(msg : types.Message, state : FSMContext):
    db.update_user_number(msg.html_text, 1)
    await msg.reply("<b>Chegirmalar bo'limi ushbu postga o'zgartirildi</b>", reply_markup=admin)
    await state.finish()