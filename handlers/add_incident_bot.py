from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import json
import shutil
from datetime import datetime

import os

from misc import dispatcher as dp
from misc import bot

from support_files import buttons as nav
from support_files import support_conf as support
from support_files import logs_send_email as log_email
from support_files import send_email
from support_files import whitelist_checker as wl_check
from support_files.incidents import insert_in_base as base
from support_files.incidents import search_db as search
from support_files.incidents import normal_address as normalize

class Incidents(StatesGroup):
    incident = State()
    incident_search_date = State()
    incident_search_address = State()


# Реакция на вход в инциденты
@dp.callback_query_handler(text="incidents")
async def incident_info(callback: CallbackQuery, state=FSMContext):
    if wl_check.whitelist_checker(callback.from_user.id, powers="users") != True:
        return

    await state.set_state(Incidents.incident)
    await callback.message.edit_text(text="Выбирете из предложенного:", reply_markup=nav.inline_reply_incident)


# 1.1 Поиск по дате
@dp.callback_query_handler(text="search_date", state=Incidents.incident)
async def search_date(callback: CallbackQuery, state=FSMContext):
    await callback.message.edit_text(text="Введите дату:")
    await state.set_state(Incidents.incident_search_date)


# 1.2 Ввод даты
@dp.message_handler(state=Incidents.incident_search_date)
async def search_date_insert(message: types.Message, state=FSMContext):

    try:
        date = datetime.strptime(message.text, '%d.%m.%Y')
        result_search = search.search_in_base(data=message.text, mode="date")
        if result_search: 
            for item in result_search:
                await bot.send_message(message.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
            await state.finish()
            await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)

        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "За данную дату преступлений не происходило.\n\nВыберите необходимую функцию:", reply_markup=nav.inline_reply_button)
            

    except ValueError:
        await bot.send_message(message.from_user.id, "Дата введена некоректно.\n\nВведите снова:", reply_markup=nav.main_button)


# 2.1 Поиск по адресу
@dp.callback_query_handler(text="search_address", state=Incidents.incident)
async def search_date(callback: CallbackQuery, state=FSMContext):
    await callback.message.edit_text(text="Введите адрес:")
    await state.set_state(Incidents.incident_search_address)


# 2.1 Ввод адреса
@dp.message_handler(state=Incidents.incident_search_address)
async def search_date_insert(message: types.Message, state=FSMContext):
    result_search = search.search_in_base(data=normalize.normalize_address(message.text), mode="address")
    if result_search:
        for item in result_search:
            await bot.send_message(message.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
        await state.finish()
        await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "По указанному адресу преступлений не происходило.\n\nВыберите необходимую функцию:", reply_markup=nav.inline_reply_button)
            

# 3.1 Вывод раскрытых
@dp.callback_query_handler(text="sort_rev_yes", state=Incidents.incident)
async def sort_yes(callback: CallbackQuery, state=FSMContext):
    result_search = search.search_in_base_revelation(mode="Да")
    for item in result_search:
        await bot.send_message(callback.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
    await state.finish()
    await bot.send_message(callback.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)

# 3.2 Вывод нераскрытых
@dp.callback_query_handler(text="sort_rev_none", state=Incidents.incident)
async def sort_none(callback: CallbackQuery, state=FSMContext):
    result_search = search.search_in_base_revelation(mode="Нет")
    for item in result_search:
        await bot.send_message(callback.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
    await state.finish()
    await bot.send_message(callback.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)


# 1     Кнопка просмотра всех эпизодов  (-)
# 1.1   Сортировка по раскрытым         (+) search_db.py
# 1.2   Сортировка по не раскрытым      (+) search_db.py
# 1.3   Посик по дате                   (+) search_db.py
# 1.4   Поиск по адресу                 (+) search_db.py


# Карточка: 1. Порядковый номер, 2. Раскрытие,      (+) 
# 3. Дата совершения, 4. Адрес совершения,           |  insert_in_base.py
# 5. Кто выезжал, 6. Фабула                         (+) 

# 1. Добавление фотографий, 2. Формирование отчета в HTML-файл  (-)

# Карточка заносится в SQL-таблицу.     (+) insert_in_base.py

# 2     Кнопка добавления новых эпизодов    ()
# 2.1   Введите кто выезжал                 ()
# 2.2   Введите дату                        ()
# 2.3   Ведите адрес                        ()
# 2.4   Введите фабулу                      ()