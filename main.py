from email import message
import logging
from socketserver import DatagramRequestHandler
from aiogram import Bot, Dispatcher, executor, types
from confing import TOKEN
from buton import menu
from states import Ustoz
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO)

bot =Bot(token=TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def do_start(messsage: types.Message,state: FSMContext):
    user = messsage.from_user.full_name
    user_id = messsage.from_user.id

    await messsage.answer(f"Assalom alaykum {user}UstozShogird kanalining rasmiy botiga xush kelibsiz!z\nid: {user_id}", reply_markup=menu)
    
@dp.message_handler(text="Sherik kerak")
async def sherik(message:types.Message):
    await message.answer("Ism, familiyangizni kiriting?",reply_markup=ReplyKeyboardRemove())
    await Ustoz.ism.set()

@dp.message_handler(state=Ustoz.ism)
async def ism(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data(
        {'ism' : ism}
    )
    await message.answer("📚 Texnologiya:\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\nJava, C++, C#")
    # await Ustoz.ism.set()
    await Ustoz.next()

@dp.message_handler(state=Ustoz.texno)
async def texno(message: types.Message, state: FSMContext):
    texno = message.text
    await state.update_data(
        {'texno' : texno}
    )
    await message.answer("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")
    await Ustoz.texno.set()
    await Ustoz.next()

@dp.message_handler(state=Ustoz.phone)
async def phone(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        phone = int(phone)
        await state.update_data(
            {'phone' : phone}
        )
        await message.answer("🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")
        await Ustoz.phone.set()  
          
        await Ustoz.next()
    except:
        await message.answer("Raqamni tog'ri kiriting")
         


@dp.message_handler(state=Ustoz.hudud)
async def hudud(message: types.Message, state: FSMContext):
    hudud = message.text
    await state.update_data(
        {"hudud": hudud}
    )
    await message.answer("💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")
    await Ustoz.hudud.set()
    await Ustoz.next()



# @dp.message_handler(state=Ustoz.hudud)
# async def hudud(message: types.Message, state: FSMContext):
#     hudud = message.text
#     await state.update_data(
#         {"hudud": hudud}
#     )
#     await message.answer("💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")
#     # await Ustoz.hudud.set()
#     await Ustoz.next()


@dp.message_handler(state=Ustoz.Narxi)
async def Narxi(message: types.Message, state: FSMContext):
    Narxi = message.text
    await state.update_data(
        {"Narxi": Narxi}
    )
    await message.answer("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba")
    await Ustoz.Narxi.set()
    await Ustoz.next()


@dp.message_handler(state=Ustoz.ish)
async def ish(message: types.Message, state: FSMContext):
    ish = message.text
    await state.update_data(
        {"ish": ish}
    )
    await message.answer("🕰 Murojaat qilish vaqti: \n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")
    await Ustoz.ish.set()
    await Ustoz.next()


@dp.message_handler(state=Ustoz.time)
async def time(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(
        {"time": time}
    )
    await message.answer("🔎 Maqsad:\n\nMaqsadingizni qisqacha yozib bering.")
    await Ustoz.time.set()
    await Ustoz.next()

@dp.message_handler(state=Ustoz.Maqsad)
async def Maqsad(message: types.Message, state: FSMContext):
    Maqsad = message.text
    await Ustoz.Maqsad.set()
    data = await state.get_data()
    ism = data.get('ism')
    texno = data.get('texno')
    phone = data.get('phone')
    hudud = data.get('hudud')
    Narxi = data.get("Narxi")
    ish = data.get("ish")
    time = data.get("time")
    Maqsad = data.get('Maqsad')
    await message.answer(f"🏅 Sherik: {ism}\n📚 Texnologiya:  {texno}\n📞 Aloqa:  +{phone}\n🌐 Hudud:  {hudud}\n💰 Narxi:  {Narxi}\n👨🏻‍💻 Kasbi:  {ish}\n🕰 Murojaat qilish vaqti:  {time}\n🔎 Maqsad:  {Maqsad}\n\n Admin @Matchanov_096 ")
    await message.answer("Barcha ma'lumotlar to'g'rimi?")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)