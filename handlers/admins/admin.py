from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.inline.aloqa import aloqa
from keyboards.default.admin_menu import admin
from data.config import ADMINS


from loader import dp, db, bot


@dp.message_handler(text="Admin", chat_id=ADMINS)
async def admin_func(msg : types.Message):
    await msg.answer("Admin panel", reply_markup=admin)