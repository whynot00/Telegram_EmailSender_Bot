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
        await callback.message.edit_text("<b>Введите номер дела (возможен ввод последних цифр):</b>")
        await state.set_state(Cases.search_case_1)

@dp.message_handler(state=[Cases.add_case_1, Cases.add_case_2, Cases.add_case_3, Cases.add_case_4])
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
        
        elif get_state == "Cases:add_case_2":
            if message.text.isdigit():
                data["num_case"] = message.text
                await bot.send_message(message.from_user.id, "Введите дату заведения:")
                await state.set_state(Cases.add_case_3)
            else:
                await bot.send_message(message.from_user.id, "КУСП введен не коректно\n\nВведите снова:")

        elif get_state == "Cases:add_case_3":
            try:
                date = datetime.strptime(message.text, '%d.%m.%Y')
                data["date_case"] = str(message.text)
                await state.set_state(Cases.add_case_4)
                await bot.send_message(message.from_user.id, "Введите статью (только цифры - Например: 159 4)")
            except ValueError:
                await bot.send_message(message.from_user.id, "Дата введена некоректно.\n\nВведите снова:")
            
        elif get_state == "Cases:add_case_4":
            data["article"] = message.text
            result_add = [data["kusp"], data["num_case"], data["date_case"], data["article"],]

            base.insert_case(result_add)
            await bot.send_message(message.from_user.id, "Уголовное дело успешно внесено!", reply_markup=nav.inline_reply_button)

            await state.finish()

@dp.message_handler(state=Cases.search_case_1)
async def search_case(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        result_search = search.search_in_base(data=message.text, mode="criminal_case")
        if result_search:
            from_req.form_story_in_html(db_list=result_search, search_title=f"Поиск по УД - {message.text}", userid=message.from_user.id, mode="default")
            await bot.send_document(message.from_user.id, open(f"user_files/Поиск по УД - {message.text}_{message.from_user.id}.html", "rb"), caption="Сформирован отчет.")
            await bot.send_message(message.from_user.id, "Главное меню.", reply_markup=nav.inline_reply_button)
            os.unlink(f"user_files/Поиск по УД - {message.text}_{str(message.from_user.id)}.html")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "<b>По данному запросу информации нет.</b>\nГлавное меню:", reply_markup=nav.inline_reply_button)
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, "<b>Номер дела введен не корректно</b>\nВведите снова:")


                