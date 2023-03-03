from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.inline.aloqa import aloqa
from keyboards.default.menu import menu
import asyncio


from loader import dp


@dp.message_handler()
async def asdf(msg : types.Message):
    await msg.answer("<b>Quyidagi tugmalardan foydalaning 👇</b>", reply_markup=menu)