from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from data.config import ADMINS


from loader import dp, db, bot, temp


@dp.message_handler(text="Kurs qo'shish", chat_id = ADMINS)
async def add_kurs(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Kurs nomini yuboring : </b>", reply_markup=bekor)
    await state.set_state("kurs_nomi")
    
@dp.message_handler(text="◀️Ortga", chat_id = ADMINS, state = ["kurs_nomi", "kurs_tarif"])
async def add_kurs(msg : types.Message, state : FSMContext):
    await msg.answer("<b><i>Menu : </i></b>", reply_markup=admin)
    await state.finish()
    

@dp.message_handler(state = "kurs_nomi", chat_id = ADMINS)
async def add_nom(msg : types.Message, state : FSMContext):
    if len(msg.text) < 31:
        temp[msg.from_user.id] = msg.text
        await msg.answer("<b>Kurs ta'rifini yuboring : </b>", reply_markup=bekor)
        await state.set_state("kurs_tarif")
    else :
        await msg.answer("<b>Juda uzun, qayta kiriting : (30 ta belgi)</b>", reply_markup=bekor)
        
@dp.message_handler(state="kurs_tarif", chat_id = ADMINS)
async def add_kurs(msg : types.Message, state : FSMContext):
    try:
        db.add_kurs(temp[msg.from_user.id], msg.html_text)
        await msg.answer("<b>Kurs muvaffaqiyatli qo'shildi ✅</b>", reply_markup=admin)
        await state.finish()
    except :
        await msg.answer("<b>Xatolik ❗️\n\n<i>Bunday nomdagi kurs bo'lishi mumkin, tekshirib ko'ring</i></b>", reply_markup=admin)
        await state.finish()