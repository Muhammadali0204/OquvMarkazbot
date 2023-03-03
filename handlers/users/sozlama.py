from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.bekor_qilish import bekor
from keyboards.default.sozlama import sozlama
from keyboards.default import contact, menu
from utils.misc import belgi


from loader import dp, db, bot

@dp.message_handler(text="🛠Sozlamalar")
async def sozlamalar(msg : types.Message, state : FSMContext):
    user = db.select_user(msg.from_user.id)
    await msg.answer(f"<b>🛠Sozlamalar\n\n👤Ismingiz : </b><i>{user[1]}</i>\n<b>☎️Telefon raqamingiz : </b><i>{user[2]}</i>", reply_markup=sozlama)
    await state.set_state("sozlamalar")
    
    
    
    
@dp.message_handler(text="◀️Ortga",state = "sozlamalar")
async def ortga1(msg : types.Message, state : FSMContext):
    await msg.answer("<b>📋<i>Menu</i></b>", reply_markup=menu.menu)
    await state.finish() 
    
@dp.message_handler(text= "♻️Ismni o'zgartirish",state = "sozlamalar")
async def ism(msg : types.Message, state : FSMContext):
    await msg.answer("<b>Yangi ism yuboring : </b>", reply_markup=bekor)
    await state.set_state("ism_tahrirla")
    
    
@dp.message_handler(text= "🔢Raqamni o'zgartirish",state = "sozlamalar")
async def ism(msg : types.Message, state : FSMContext):
    await msg.answer(f"<b>Raqamingizni yuboring : </b>\n\n❗<b>Siz bilan bog'lana olishimiz uchun, iltimos faol raqamingizni yuboring.</b>\n<i>+998901234567 ko'rinishida yoki shu telegram akkountingiz raqamidan foydalanayotgan bo'lsangiz </i><u><b>🔢Raqamimni yuborish</b></u><i> tugmasini bosing.</i>", reply_markup=contact.contact2)
    await state.set_state("raqam2")
    
    
@dp.message_handler(state = "sozlamalar")
async def boshqa(msg : types.Message):
    await msg.delete()
    await msg.answer("<b>Quyidagi tugmalardan foydalaning 👇</b>", reply_markup=sozlama)
    
    
    
    
     
    
@dp.message_handler(text="◀️Ortga",state = "ism_tahrirla")
async def ortga1(msg : types.Message, state : FSMContext):
    await msg.answer("<b>🛠Sozlamalar</b>", reply_markup=sozlama)
    await state.set_state("sozlamalar")
    
@dp.message_handler(text="◀️Ortga",state = "raqam2")
async def ortga1(msg : types.Message, state : FSMContext):
    await msg.answer("<b>🛠Sozlamalar</b>", reply_markup=sozlama)
    await state.set_state('sozlamalar')
    
    
    
@dp.message_handler(state="raqam2")
async def contact_msg(msg : types.Message, state : FSMContext):
    if msg.text.startswith('+998') and len(msg.text) == 13 and msg.text[1:].isnumeric():
        db.update_user_number(msg.text, msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli o'zgartirildi ✅</b>")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    else:
        await msg.answer("<b>Xato telefon raqami ❗\n\n<i>Iltimos raqamingizni qayta yuboring.</i></b>", reply_markup=contact.contact2)
        
@dp.message_handler(content_types=types.ContentType.CONTACT, state = 'raqam2')
async def contact_user(msg : types.Message, state : FSMContext):
    raqam = msg.contact.phone_number
    if raqam.startswith("+998"):
        db.update_user_number(raqam, msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli o'zgartirildi ✅</b>")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    elif raqam.startswith("998"):
        db.update_user_number(f"+{raqam}", msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli o'zgartirildi ✅</b>")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
    else:
        db.update_user_number(raqam, msg.from_user.id)
        await msg.answer("<b>Raqamingiz muvaffaqiyatli o'zgartirildi ✅</b>\n\nLekin raqamingiz yaroqsiz ❌")
        await msg.answer("<b><i>📋Menu : </i></b>", reply_markup=menu.menu)
        await state.finish()
        
    
@dp.message_handler(state = "ism_tahrirla")
async def ism_tahrir(msg : types.Message, state : FSMContext):
    if all(x.isalpha() or belgi.belgi(x) for x in msg.text):
        if len(msg.text) < 101 and len(msg.text) > 2:
            db.update_user_name(msg.text, msg.from_user.id)
            await msg.answer(f"<b>Ismingiz muvaffaqiyatli o'zgartirildi ✅</b>", reply_markup=menu.menu)
            await state.finish()
        elif len(msg.text) > 100:
            await msg.answer("<b>Juda uzun, qayta yuboring : </b>", reply_markup=bekor)
        else :
            await msg.answer("<b>Juda qisqa qayta yuboring : </b>", reply_markup=bekor)
    else:
        await msg.answer("<b>Faqat lotin harflari, bo'sh joy yoki (' `) belgilaridan foydalanishingiz mumkin❗</b>\n\n<i>Qayta kiriting : </i>", reply_markup=bekor)