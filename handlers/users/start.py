from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.misc import belgi
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default import menu, contact


from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state : FSMContext):
    user = db.select_user(message.from_user.id)
    if user == None:
        db.add_user(message.from_user.id, message.from_user.full_name, None)
        await message.answer(f"<b><i>Assalomu alaykum {message.from_user.get_mention(message.from_user.full_name)}</i>\n\n<u>ASIA</u> o'quv markazining telegram botiga botiga xush kelibsiz!</b>")
        await message.answer("<b>Ism-familiyangizni yuboring : </b>")
        await state.set_state("ism")
    else:
        await message.answer(f"<b>Assalomu alaykum <i>{message.from_user.get_mention(message.from_user.full_name)}</i></b>")
        await message.answer("<i>📋Menu : </i>", reply_markup=menu.menu)
  
    
    
@dp.message_handler(state="ism")
async def ismi(msg : types.Message, state : FSMContext):
    if all(x.isalpha() or belgi.belgi(x) for x in msg.text):
        if len(msg.text) < 101 and len(msg.text) > 2:
            db.update_user_name(msg.text, msg.from_user.id)
            await msg.answer(f"<b>Raqamingizni yuboring : </b>\n\n❗<b>Siz bilan bog'lana olishimiz uchun, iltimos faol raqamingizni yuboring.</b>\n<i>+998901234567 ko'rinishida yoki shu telegram akkauntingiz raqamidan foydalanayotgan bo'lsangiz </i><u><b>🔢Raqamimni yuborish</b></u><i> tugmasini bosing.</i>", reply_markup=contact.contact)
            await state.set_state("raqam")
        elif len(msg.text) > 100:
            await msg.answer("<b>Juda uzun, qayta yuboring : </b>")
        else :
            await msg.answer("<b>Juda qisqa qayta yuboring : </b>")
    else:
        await msg.answer("<b>Faqat lotin harflari, bo'sh joy yoki (' `) belgilaridan foydalanishingiz mumkin❗</b>\n\n<i>Qayta kiriting : </i>")
        
        
@dp.message_handler(state="raqam")
async def contact_msg(msg : types.Message, state : FSMContext):
    if msg.text.startswith('+998') and len(msg.text) == 13 and msg.text[1:].isnumeric():
        db.update_user_number(msg.text, msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅</b>")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    else:
        await msg.answer("<b>Xato telefon raqami ❗\n\n<i>Iltimos raqamingizni qayta yuboring.</i></b>")
        
@dp.message_handler(content_types=types.ContentType.CONTACT, state = 'raqam')
async def contact_user(msg : types.Message, state : FSMContext):
    raqam = msg.contact.phone_number
    if raqam.startswith("+998"):
        db.update_user_number(raqam, msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅</b>")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    elif raqam.startswith("998"):
        db.update_user_number(f"+{raqam}", msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅</b>")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    else:
        db.update_user_number(raqam, msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅\n\nLekin bu raqamingiz yaroqsiz ❌</b>")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    