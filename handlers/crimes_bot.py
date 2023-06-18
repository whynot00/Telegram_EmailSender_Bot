from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import shutil
from datetime import datetime

import os

from misc import dispatcher as dp
from misc import bot

from support_files import buttons as nav
from support_files import logs as lg
from support_files import send_email
from support_files import check_date
from support_files import whitelist_checker as wl_check
from support_files.incidents import insert_in_base as base
from support_files.incidents import search_db as search
from support_files.incidents import normal_address as normalize
from support_files.incidents import form_request as from_req


class Crimes(StatesGroup):
    search_name = State()
    add_name_1 = State()
    add_name_2 = State()
    add_name_3 = State()
    add_name_4 = State()

@dp.callback_query_handler(text="crimes")
async def crimes_menu(callback: CallbackQuery):
    await callback.message.edit_text("<b>Выберите действие:</b>", reply_markup=nav.inline_reply_crimes_names)
    await callback.answer()

@dp.callback_query_handler(text=["search_crimes_name", "add_crimes_name"])
async def search_add_crimes(callback: CallbackQuery, state=FSMContext):
    if callback.data == "search_crimes_name":
        await callback.message.edit_text("<b>Введите ФИО лица:</b>")
        await state.set_state(Crimes.search_name)

    elif callback.data == "add_crimes_name":
        if wl_check.whitelist_checker(callback.from_user.id, powers="moderator") == True:
            await callback.message.edit_text("<b>Введите ФИО лица:</b>")
            await state.set_state(Crimes.add_name_1)
        else:
            await callback.message.edit_text("<b>У вас недостаточно прав.</b>", reply_markup=nav.inline_reply_button)
    
    await callback.answer()

@dp.message_handler(state=[Crimes.add_name_1, Crimes.add_name_2, Crimes.add_name_3])
async def crimes_messages(message: types.Message, state=FSMContext):
    get_state = await state.get_state()
    
    async with state.proxy() as data:
        if get_state == "Crimes:add_name_1":
            data["name"] = message.text
            await bot.send_message(message.from_user.id, "<b>Введите год рождения лица:</b>")
            await state.set_state(Crimes.add_name_2)
        
        if get_state == "Crimes:add_name_2":
            if check_date.check_date(str(message.text)) == True:
                data["date"] = message.text
                await bot.send_message(message.from_user.id, "<b>Введите дату задержания лица:</b>")
                await state.set_state(Crimes.add_name_3)
            else:
                await bot.send_message(message.from_user.id, "Дата введена не корректно.\n<b>Введите снова:</b>")
        
        if get_state == "Crimes:add_name_3":
            if check_date.check_date(str(message.text)) == True:
                data["date_crimes"] = message.text
                await bot.send_message(message.from_user.id, "<b>Введите статус задержанного лица:</b>", reply_markup=nav.inline_reply_incident_confirm_story)
                await state.set_state(Crimes.add_name_4)
            else:
                await bot.send_message(message.from_user.id, "<b>Дата введена не корректно.\nВведите снова:</b>")

        if get_state == "Crimes:add_name_4":
            data["status_crime"] = message.text
            await bot.send_message(message.from_user.id, f"<b>Проверьте верность введеной информации</b>\n\n<b>ФИО: </b>{data['name']}\n<b>Год рождения: </b>{data['date']}\n<b>Дата задержания: </b>{data['date_crimes']}\n<b>Статус: </b>{data['status_crime']}", reply_markup=nav.inline_reply_incident_confirm_story)


@dp.callback_query_handler(text=["add_photo_incident", "confirm_add_incident"], state=Crimes.add_name_4)
async def confirm_add(callback: CallbackQuery, state=FSMContext):
    if callback.data == "add_photo_incident":
        await bot.send_message(callback.from_user.id, "Данная функция пока не доступна.")
    
    if callback.data == "confirm_add_incident":
        await bot.send_message(callback.from_user.id, '<b>Карточка успешно добавлена.</b>\n\nУказать эпизоды которые есть за данным лицом, можно во вкладке "Поиск по ID".', reply_markup=nav.inline_reply_button)
        await state.finish()

    await callback.answer()

