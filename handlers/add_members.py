from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import json
import os

from support_files import buttons as nav
from misc import dispatcher as dp
from misc import bot

from support_files import buttons as nav
from support_files import whitelist_checker as wl_check

class Members(StatesGroup):
    add_msg = State()


# Реакция на /members
@dp.message_handler(commands="mem")
async def mem(message: types.Message, state=FSMContext):
    await state.set_state(Members.add_msg)
    if wl_check.whitelist_checker(message.from_user.id, powers="admin") != True:
        await bot.send_message(message.from_user.id, "У вас недостаточно прав.")
        return
    with open("configurations/white_list.json", "r") as file:
        members = json.load(file)
        msg = await bot.send_message(message.from_user.id, f"Администраторы:\n{members['admin']}\n\nПользователи:\n{members['users']}", reply_markup=nav.inline_reply_members)
    async with state.proxy() as data:
        data["msg_id"] = msg.message_id


# Реакция на добавление пользователя
@dp.callback_query_handler(text="add_member", state=Members.add_msg)
async def add_member(message: types.Message, state=FSMContext):
    # async with state.proxy() as data:
    #     await bot.delete_message(message.from_user.id, data["msg_id"])
    #     msg = await bot.send_message(message.from_user.id, "Выберете полномочия:", reply_markup=nav.inline_reply_addmem)



