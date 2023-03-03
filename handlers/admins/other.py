from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.menu import menu
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from data.config import ADMINS
import datetime, pytz


from loader import dp, db, bot, temp


@dp.message_handler(text="Foydalanuvchilar soni", chat_id = ADMINS)
async def soni(msg : types.Message):
    await msg.answer(f"<b>Botdan foydalanuvchilar soni : <i>{db.count_users()[0] - 1}</i> ta</b>")
    
@dp.message_handler(text="Menu", chat_id = ADMINS)
async def menu1(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Foydalanuvchilar menusi : </b>", reply_markup=menu)
    
@dp.callback_query_handler(regexp="wrong_number+")
async def xato_raqam(call : types.CallbackQuery):
    id = call.data.split(':')[1]
    answer = f"<b>Botga kiritgan raqamingiz orqali sizga bog'lana olmadik\n\nIltimos, sizga bog'lana olishimiz mumkin bo'lgan raqamingizni botga kiriting❗️</b>"
    await bot.send_message(id, answer)
    message = call.message.html_text
    t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
    time = t.strftime("%H:%M %d.%m.%Y")
    answer = f"{message}\n\n<b>Ko'rib chiqildi : </b>\n<i>Noto'g'ri raqam ❌\n\n{time}</i>"
    await call.message.edit_text(answer)
    
@dp.callback_query_handler(text="ok")
async def ok(call : types.CallbackQuery):
    message = call.message.html_text
    t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
    time = t.strftime("%H:%M %d.%m.%Y")
    answer = f"{message}\n\n<b>Ko'rib chiqildi </b>✅\n\n<i>{time}</i>"
    await call.message.edit_text(answer)
    