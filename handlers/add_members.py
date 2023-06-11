from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import json

from misc import dispatcher as dp
from misc import bot

from support_files import logs as lg
from support_files import buttons as nav
from support_files import whitelist_checker as wl_check


class Members(StatesGroup):
    add_btn_1 = State()
    add_btn_2 = State()
    delete_btn_1 = State()
    delete_btn_2 = State()


# Реакция на /members
@dp.message_handler(commands="members")
async def members(message: types.Message):
    if wl_check.whitelist_checker(message.from_user.id, powers="admin") != True:
        await bot.send_message(message.from_user.id, "У вас недостаточно прав.")
        return
    with open("configurations/white_list.json", "r") as file:
        members = json.load(file)
    
    await bot.send_message(message.from_user.id, f"Администраторы:\n{members['admin']}\n\nПользователи:\n{members['users']}", reply_markup=nav.inline_reply_members)


# 1.1 - Реакция на выбор добавления
@dp.callback_query_handler(text="add_member")
async def add_member(callback: CallbackQuery, state=FSMContext):
    await callback.message.edit_text(text="Выберите полномочия:", reply_markup=nav.inline_reply_addmem)
    await state.set_state(Members.add_btn_1)


# 1.2 - Реакция на добавление администратора
@dp.callback_query_handler(text="admin_btn", state=Members.add_btn_1)
async def add_btn_users(callback: CallbackQuery, state=FSMContext):
    with open("configurations/white_list.json", "r") as file:
        await callback.message.edit_text(text="Введите ID пользователя:")
    async with state.proxy() as data:
        data["powers"] = "admin"


# 1.3 - Реакция на добавление пользователя
@dp.callback_query_handler(text="user_btn", state=Members.add_btn_1)
async def add_btn_users(callback: CallbackQuery, state=FSMContext):
    with open("configurations/white_list.json", "r") as file:
        await callback.message.edit_text(text="Введите ID пользователя:")
    async with state.proxy() as data:
        data["powers"] = "users"


# 1.4 - Реакция ввода и ожидание подтверждения
@dp.message_handler(state=Members.add_btn_1)
async def add_btn_confirm(message: types.Message, state=FSMContext):
    if message.text.isdigit() == True:
        await state.set_state(Members.add_btn_2)
        with open("configurations/white_list.json", "r") as file:
            member = json.load(file)

        async with state.proxy() as data:
            data["ID"] = message.text
            if data["powers"] == "admin":
                member[data["powers"]].append(message.text)
            elif data["powers"] == "users":
                member[data["powers"]].append(message.text)

            data["confrim"] = member

        await bot.send_message(message.from_user.id, f"Подтвердите добавление пользователя пользователя: {message.text}", reply_markup=nav.add_button)
    else:
        await bot.send_message(message.from_user.id, "ID введен некоректно. Введите снова:")


# 1.5 - Общая функция для ввода ID администратора или пользователя
@dp.message_handler(text=nav.add_btn.text, state=Members.add_btn_2)
async def add_member_btn(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        with open("configurations/white_list.json", "w") as file:   
            json.dump(data["confrim"], file)

    await bot.send_message(message.from_user.id, f"ID пользователя внесен, в категорию {data['powers']}", reply_markup=types.ReplyKeyboardRemove())

    logs_infomation = [message.from_user.username, message.from_user.id, "add_user", data["ID"]]
    lg.logs(data_dict=logs_infomation, action="change_powers")


    await state.finish()
    

# 2.1 - Реакция на удаление пользователя
@dp.callback_query_handler(text="delete_member")
async def delete_member(callback: CallbackQuery, state=FSMContext):
    await state.set_state(Members.delete_btn_1)
    await bot.send_message(callback.from_user.id, "Введите ID пользователя, которого необходимо удалить.\nНевозможно удалить адмимистратора", reply_markup=nav.main_button)


# 2.2 - Реакция на получение ID пользователя
@dp.message_handler(state=Members.delete_btn_1)
async def delete_btn(message: types.Message, state=FSMContext):
    with open("configurations/white_list.json", "r") as file:
        member = json.load(file)

    if message.text in member["users"]:
        await bot.send_message(message.from_user.id, f"Подтвердите удаление пользователя: {message.text}", reply_markup=nav.delete_button)
        member["users"].remove(message.text)
        await state.set_state(Members.delete_btn_2)
    else:
        await bot.send_message(message.from_user.id, "Такого пользователя нет.", reply_markup=nav.main_button)
    
    async with state.proxy() as data:
        data["members_removed"] = member
        data["ID"] = message.text

    


# 2.3 - Реакция на подтверждение удаления
@dp.message_handler(text=nav.delete_btn.text, state=Members.delete_btn_2)
async def delete_btn_confirm(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(data["members_removed"])
        with open("configurations/white_list.json", "w") as file:
            json.dump(data["members_removed"], file)

    await bot.send_message(message.from_user.id, "Пользователь успешно удален!", reply_markup=types.ReplyKeyboardRemove())

    logs_infomation = [message.from_user.username, message.from_user.id, "delete_user", data["ID"]]
    lg.logs(data_dict=logs_infomation, action="change_powers")

    await state.finish()