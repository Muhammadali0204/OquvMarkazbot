from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from data.config import ADMINS
import asyncio


from loader import dp, db, bot, temp


@dp.message_handler(text="Kursni tahrirlash", chat_id = ADMINS)
async def edit(msg : types.Message, state : FSMContext):
    data = db.select_all_kurs()
    if data != []:
        await msg.answer('<b>Kursni tahrirlash</b>', reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("<b>Tahrirlamoqchi bo'lgan kursni tanlang : </b>", reply_markup=kurslar(data))
        await state.set_state('edit_kurs')
    else:
        await msg.answer("<b>Kurslar mavjud emas</b>")
        
        
@dp.callback_query_handler(state='edit_kurs', text="back")
async def delete(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<i>Menu : </i>", reply_markup=admin)
    await state.finish()
        
@dp.callback_query_handler(state='edit_kurs')
async def delete(call : types.CallbackQuery, state : FSMContext):
    data = call.data
    kurs = db.select_kurs(data)
    try:
        await call.message.answer(f"<b>Kursning hozirgi holdagi ta'rifi : \n\n</b>{kurs[2]}\n\n<i>Yangi ta'rifni yuboring : </i>")
        temp[call.from_user.id] = data
        await call.message.delete()
        await state.set_state("edit_kurs2")
    except:
        await call.message.delete()
        await call.message.answer("Xatolik!", reply_markup=admin)
        await state.finish()

@dp.message_handler(state="edit_kurs")
async def messagee(msg : types.Message):
    await msg.delete()
    await msg.answer("<b>Menuga qaytish uchun 🔙Ortga tugmasini bosing.</b>")
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, (msg.message_id + 1))
        
        
@dp.message_handler(state='edit_kurs2')
async def edit(msg : types.Message, state : FSMContext):
    try:
        db.update_tarif(temp[msg.from_user.id], msg.html_text)
        await msg.answer(f"<b>Muvaffaqiyatli o'zgartirildi ✅</b>", reply_markup=admin)
        await state.finish()
    except:
        await msg.answer("Xatolik!", reply_markup=admin)
        await state.finish()
        
        
