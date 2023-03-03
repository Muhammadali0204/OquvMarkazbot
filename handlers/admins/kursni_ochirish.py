from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from data.config import ADMINS
import asyncio


from loader import dp, db, bot, temp


@dp.message_handler(text="Kursni o'chirish", chat_id = ADMINS)
async def delete_kurs(msg : types.Message, state : FSMContext):
    data = db.select_all_kurs()
    if data != []:
        await msg.answer("<b>O'chirmoqchi bo'lgan kursni tanlang : </b>", reply_markup=kurslar(data))
        await state.set_state('delete_kurs')
    else:
        await msg.answer("<b>Kurslar mavjud emas</b>")
        
     
@dp.callback_query_handler(state='delete_kurs', text="back")
async def delete(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<i>Menu : </i>", reply_markup=admin)
    await state.finish()
    
@dp.message_handler(state="delete_kurs")
async def messagee(msg : types.Message):
    await msg.delete()
    await msg.answer("<b>Menuga qaytish uchun 🔙Ortga tugmasini bosing.</b>")
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, (msg.message_id + 1))
        
@dp.callback_query_handler(state='delete_kurs')
async def delete(call : types.CallbackQuery, state : FSMContext):
    data = call.data
    kurs = db.select_kurs(data)
    try:
        db.delete_kurs(data)
        await call.message.answer(f"<b>{kurs[1]} - kursi o'chirildi❗</b>", reply_markup=admin)
        await call.answer(f"{kurs[1]} - kursi o'chirildi❗")
        await call.message.delete()
        await state.finish()
    except:
        await call.message.delete()
        await call.message.answer("Xatolik!", reply_markup=admin)
        await state.finish()