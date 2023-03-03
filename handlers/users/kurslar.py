from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.inline.aloqaga_chiq import aloqa_keyboard
from keyboards.inline.aloqa import aloqa
from keyboards.default.menu import menu
from data.config import ADMINS
import asyncio


from loader import dp, db, bot


@dp.message_handler(text="📚Bizning kurslarimiz")
async def kurss(msg : types.Message, state : FSMContext):
    data = db.select_all_kurs()
    if data != []:
        await msg.answer(f"<b>📚Kurslarimiz soni : </b><i>{len(data)} ta</i>", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("<b>📚Bizning kurslarimiz : </b>", reply_markup=kurslar(data))
        await state.set_state('kurslar')
    else:
        await msg.answer("<b>Kurslar mavjud emas</b>")
    
    
@dp.callback_query_handler(text="back", state='kurslar')
async def menuu(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<i>Menu : </i>", reply_markup=menu)
    await state.finish()
    
@dp.message_handler(state="kurslar")
async def messagee(msg : types.Message):
    await msg.delete()
    await msg.answer("<b>Bosh menuga qaytish uchun 🔙Ortga tugmasini bosing.</b>")
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, (msg.message_id + 1))
    
@dp.callback_query_handler(state='kurslar')
async def tarif(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    data = call.data
    kurs = db.select_kurs(data)
    user = db.select_user(call.from_user.id)
    answer = f"<b>📕Kurs nomi : {kurs[1]}</b>\n\n{kurs[2]}\n\n<i>📕Kurs haqida qo'shimcha ma'lumot olishni istasangiz, operatorimiz siz bilan bog'lanishi mumkin.\nBuning uchun quyidagi tugmani bosing : \n\n*Sizning raqamingiz : <u>{user[2]}</u>, boshqa raqamga qo'ng'iroq qilishimizni xohlasangiz 🛠Sozlamalar bo'limidan raqamingizni o'zgartiring.</i>"
    await call.message.answer(answer, reply_markup=aloqa(f"aloqa:{kurs[1]}"), disable_web_page_preview=True)
    await call.message.answer("<i>Menu : </i>", reply_markup=menu)
    await state.finish()
    
    
@dp.callback_query_handler(regexp="aloqa:+")
async def aloqa1(call : types.CallbackQuery):
    kurs = call.data.split(":")[1]
    user = db.select_user(call.from_user.id)
    username = call.from_user.username
    if username == None:
        username = "Username mavjud emas"
    else :
        username = f"@{username}"
    answer = f"<b>Foydalanuvchi <u>{user[1]}</u> <u>{kurs}</u> kursi uchun aloqaga chiqishni so'radi\n\nTelefon raqam : <i>{user[2]}</i>\nUsername : <i>{username}</i></b>"
    await call.message.answer(f"<b>{kurs} kursi bo'yicha so'rovingiz yuborildi✅\n\n<i>Operatorlarimiz tez orada <u>{user[2]}</u> raqamingizga aloqaga chiqishadi.</i></b>")
    await call.message.delete()
    await bot.send_message(ADMINS[0], answer, reply_markup=aloqa_keyboard(call.from_user.id))