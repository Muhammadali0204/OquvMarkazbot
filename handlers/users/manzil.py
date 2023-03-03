from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.kurslar import kurslar
from keyboards.inline.aloqa import aloqa
from keyboards.default.menu import menu
import asyncio


from loader import dp, db, bot


@dp.message_handler(text="📍Manzilimiz")
async def manzil(msg : types.Message):
    await msg.answer("<b>🏢Manzil: Andijon shahar Muqumiy ko'chasi 35\nMo'ljal:  'MUMTOZ' savdo majmuasi, 'SIM SIM' kafesi qarshisida</b>")
    await msg.answer_location(40.759047, 72.354358)
    
@dp.message_handler(text="🔗Biz bilan bog'lanish")
async def boglan(msg : types.Message):
    await msg.answer("<b>Murojaat uchun telefon raqamlari :\n\n☎️+998940500093\n☎️+998946389778</b>")
    