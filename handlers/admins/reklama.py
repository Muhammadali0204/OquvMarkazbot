from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.default.admin_menu import admin
from keyboards.default.bekor_qilish import bekor
from data.config import ADMINS
import asyncio


from loader import dp, db, bot, temp
    
@dp.message_handler(text="Reklama", chat_id = ADMINS)
async def reklama(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Yaxshi, reklama postini yuboring : </b>\n<i>(Text, Rasm, Video, Dokument)</i>\n<i>❗️Yuborgan postingiz shu holicha barcha foydalanuvchilarga yuboriladi\nOrtga qaytishingiz ham mumkin</i>", reply_markup=bekor)
    await state.set_state("r")
    
@dp.message_handler(text="◀️Ortga", state = "r")
async def ortga(msg : types.Message, state : FSMContext):
    await msg.answer("<b><i>Menu : </i></b>", reply_markup=admin)
    await state.finish()
    
@dp.message_handler(state = "r", content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.TEXT, types.ContentType.DOCUMENT])
async def reklama2(msg : types.Message, state : FSMContext):
    data_users = db.select_all_users()
    n = 0
    for user in data_users:
        try : 
            await bot.copy_message(user[0], msg.from_user.id, msg.message_id)
            await asyncio.sleep(0.05)
        except :
            n += 1
    await msg.answer(f"<b>✅Yuborildi : <i>{len(data_users) - n}</i>\n❌Yuborilmadi : <i>{n}</i></b>", reply_markup=admin)
    await state.finish()
    