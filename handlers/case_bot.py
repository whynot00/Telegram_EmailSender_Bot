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
from support_files.incidents import form_request as from_req

class Cases(StatesGroup):
    add_case_1 = State()
    add_case_2 = State()
    add_case_3 = State()
    add_case_4 = State()
    add_case_5 = State()
    search_case_1 = State()


@dp.callback_query_handler(text=["case", "add_case", "search_case"])
async def case_num(callback: CallbackQuery, state=FSMContext):
    if callback.data == "case":
        await callback.message.edit_text("Выберите:", reply_markup=nav.inline_reply_case)

    if callback.data == "add_case":
        await callback.message.edit_text("Введите КУСП:")
        await state.set_state(Cases.add_case_1)

    if callback.data == "search_case":
        await callback.message.edit_text("<b>Введите номер дела:</b>")
        await state.set_state(Cases.search_case_1)

@dp.message_handler(state=[Cases.add_case_1, Cases.add_case_2, Cases.add_case_3, Cases.add_case_4, Cases.search_case_1])
async def state_cases(message: types.Message, state=FSMContext):
    get_state = await state.get_state()
    async with state.proxy() as data:

        if get_state == "Cases:add_case_1":
            if message.text.isdigit():
                data["kusp"] = message.text
                await bot.send_message(message.from_user.id, "Введите номер уголовного дела (только цифры):")
                await state.set_state(Cases.add_case_2)
            else:
                await bot.send_message(message.from_user.id, "КУСП введен не коректно\n\nВведите снова:")
        
        if get_state == "Cases:add_case_2":
            if message.text.isdigit():
                data["num_case"] = message.text
                await bot.send_message(message.from_user.id, "Введите дату заведения:")
                await state.set_state(Cases.add_case_3)
            else:
                await bot.send_message(message.from_user.id, "КУСП введен не коректно\n\nВведите снова:")

        if get_state == "Cases:add_case_3":
            try:
                date = datetime.strptime(message.text, '%d.%m.%Y')
                data["date_case"] = str(message.text)
                await state.set_state(Cases.add_case_4)
                await bot.send_message(message.from_user.id, "Введите статью (только цифры - Например: 159 4)")
            except ValueError:
                await bot.send_message(message.from_user.id, "Дата введена некоректно.\n\nВведите снова:")
            
        if get_state == "Cases:add_case_4":
            data["article"] = message.text
            result_add = [data["kusp"], data["num_case"], data["date_case"], data["article"],]

            base.insert_case(result_add)
            await bot.send_message(message.from_user.id, "Уголовное дело успешно внесено!", reply_markup=nav.inline_reply_button)

            await state.finish()

        if get_state == "Cases:search_case_1":
            await state.finish()


                