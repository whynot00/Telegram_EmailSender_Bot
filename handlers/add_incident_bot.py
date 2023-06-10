from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import json
import shutil

import os
from support_files import buttons as nav
from misc import dispatcher as dp
from misc import bot

from support_files import support_conf as support
from support_files import logs_send_email as log_email
from support_files import send_email
from support_files import whitelist_checker as wl_check


   # Реакция на выход с отправки /// хз как работает на нескольких этапах????
@dp.message_handler(text=nav.main_button_2.text, state="*")
async def poyti_nahooi(message: types.Message, state=Form.button_send):
    await state.finish()
    await bot.send_message(message.from_user.id, "Выход в галвное меню.", reply_markup=types.ReplyKeyboardRemove())
    if os.path.exists(f"user_files/{message.from_user.id}") == True:
        shutil.rmtree(f"user_files/{str(message.from_user.id)}")
    if message.from_user.id in support.user_id_for_send:
        support.user_id_for_send.remove(message.from_user.id)
    await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button) 


