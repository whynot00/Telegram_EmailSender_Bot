from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from misc import dispatcher as dp
from misc import bot

from support_files import send_email
from support_files import buttons as nav

class Form_group(StatesGroup):
    chek_user = State()


    # Реакция на выход с отправки /// хз как работает на нескольких этапах????
@dp.message_handler(text=nav.main_button_2.text, state="*")
async def poyti_nahooi(message: types.Message, state="*"):
    await state.finish()
    await bot.send_message(message.from_user.id, "Выход в галвное меню.", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)


@dp.callback_query_handler(text="find_group")
async def start_find(message: types.Message, state=FSMContext):
    await state.set_state(Form_group.chek_user)
    await bot.send_message(message.from_user.id, "Отправьте никнейм пользователя:", reply_markup=nav.main_button)

@dp.message_handler(state=Form_group)
async def find_group(message: types.Message, state=FSMContext):
    ff = await bot.get_chat_member(user_id=981397216, chat_id=1938559321)
    print(ff)