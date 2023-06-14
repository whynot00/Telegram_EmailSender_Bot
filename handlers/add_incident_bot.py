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
from support_files import whitelist_checker as wl_check
from support_files.incidents import insert_in_base as base
from support_files.incidents import search_db as search
from support_files.incidents import normal_address as normalize
from support_files.incidents import form_request as from_req

class Incidents(StatesGroup):
    incident_search_geo = State()
    incident_search_date = State()
    incident_search_address = State()
    incident_search_id = State()



# Реакция на вход в инциденты
@dp.callback_query_handler(text="incidents")
async def incident_info(callback: CallbackQuery, state=FSMContext):
    if wl_check.whitelist_checker(callback.from_user.id, powers="users") != True:
        return

    await callback.message.edit_text(text="Выбирете из предложенного:", reply_markup=nav.inline_reply_incident)

# 7.1 Поиск по точке на карте
@dp.callback_query_handler(text="search_geo")
async def search_geo(callback: CallbackQuery, state=FSMContext):
    await callback.message.edit_text(text="Отправьте необходимую геолокацию:")
    await state.set_state(Incidents.incident_search_geo)

# 7.2 Ввод геолокации
@dp.message_handler(content_types="location", state=Incidents.incident_search_geo)
async def loc_handler(message, state=FSMContext):  
    coordinates = message.location.latitude, message.location.longitude
    result_search = search.search_in_base(data=coordinates, mode="locate")

    if result_search: 
            if len(result_search) <= 2:
                for item in result_search:
                    await bot.send_message(message.from_user.id, f"Расстояние до выбранной точки: {item[6]} метров\n\nID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
                await state.finish()
                await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
            else:
                from_req.form_story_in_html(db_list=result_search, search_title="Поиск по локации (радиус 1 км)", userid=message.from_user.id, mode="locate")
                await bot.send_document(message.from_user.id, open(f"user_files/Поиск по локации (радиус 1 км)_{message.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
                await bot.send_message(message.from_user.id, "Главное меню.", reply_markup=nav.inline_reply_button)
                await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "В радиусе 1 км по данным координатам преступлений не было.", reply_markup=nav.inline_reply_button)




# 1.1 Поиск по дате
@dp.callback_query_handler(text="search_date")
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
            if len(result_search) <= 2:
                for item in result_search:
                    await bot.send_message(message.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
                await state.finish()
                await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
            else:
                from_req.form_story_in_html(db_list=result_search, search_title="Поиск по дате", userid=message.from_user.id, mode="default")
                await bot.send_document(message.from_user.id, open(f"user_files/Поиск по дате_{message.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
                await bot.send_message(message.from_user.id, "Главное меню.", reply_markup=nav.inline_reply_button)
                await state.finish()
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "За данную дату преступлений не происходило.\n\nВыберите необходимую функцию:", reply_markup=nav.inline_reply_button)
        
        logs_infomation = [message.from_user.username, message.from_user.id, "story_search_date", message.text]
        lg.logs(data_dict=logs_infomation, action="incidents")
    except ValueError:
        await bot.send_message(message.from_user.id, "Дата введена некоректно.\n\nВведите снова:", reply_markup=nav.main_button)


# 2.1 Поиск по адресу
@dp.callback_query_handler(text="search_address")
async def search_date(callback: CallbackQuery, state=FSMContext):
    await callback.message.edit_text(text="Введите адрес:")
    await state.set_state(Incidents.incident_search_address)


# 2.1 Ввод адреса
@dp.message_handler(state=Incidents.incident_search_address)
async def search_date_insert(message: types.Message, state=FSMContext):
    result_search = search.search_in_base(data=normalize.normalize_address(message.text), mode="address")
    if result_search:
        if len(result_search) <= 2:
            for item in result_search:
                await bot.send_message(message.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
            await state.finish()
            await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
        else:
            from_req.form_story_in_html(db_list=result_search, search_title="Поиск по адресу", userid=message.from_user.id, mode="default")
            await bot.send_document(message.from_user.id, open(f"user_files/Поиск по адресу_{message.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
            await bot.send_message(message.from_user.id, "Главное меню.", reply_markup=nav.inline_reply_button)
            await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "По указанному адресу преступлений не происходило.\n\nВыберите необходимую функцию:", reply_markup=nav.inline_reply_button)
    
    logs_infomation = [message.from_user.username, message.from_user.id, "story_search_address", message.text]
    lg.logs(data_dict=logs_infomation, action="incidents")


# 3.1 Вывод раскрытых
@dp.callback_query_handler(text="sort_rev_yes")
async def sort_yes(callback: CallbackQuery, state=FSMContext):
    result_search = search.search_in_base_revelation(mode="Да")
    if len(result_search) <= 2:
        for item in result_search:
            await bot.send_message(callback.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
        await state.finish()
        await bot.send_message(callback.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
    else:
        from_req.form_story_in_html(db_list=result_search, search_title="Раскрытые преступления", userid=callback.from_user.id, mode="default")
        await bot.send_document(callback.from_user.id, open(f"user_files/Раскрытые преступления_{callback.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
        await bot.send_message(callback.from_user.id, "Главное меню.", reply_markup=nav.inline_reply_button)
        await state.finish()

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    logs_infomation = [callback.from_user.username, callback.from_user.id, "story_sort_revelation", "yes"]
    lg.logs(data_dict=logs_infomation, action="incidents")

# 3.2 Вывод нераскрытых
@dp.callback_query_handler(text="sort_rev_none")
async def sort_none(callback: CallbackQuery, state=FSMContext):
    result_search = search.search_in_base_revelation(mode="Нет")
    if len(result_search) <= 2:
        for item in result_search:
            await bot.send_message(callback.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
        await state.finish()
        await bot.send_message(callback.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
    else:
        from_req.form_story_in_html(db_list=result_search, search_title="Нераскрытые преступления", userid=callback.from_user.id, mode="default")
        await bot.send_document(callback.from_user.id, open(f"user_files/Нераскрытые преступления_{callback.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
        await bot.send_message(callback.from_user.id, "Главное меню.", reply_markup=nav.inline_reply_button)
        await state.finish()

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    logs_infomation = [callback.from_user.username, callback.from_user.id, "story_sort_all_incidents", "all_inicdents"]
    lg.logs(data_dict=logs_infomation, action="incidents")

# 5.1 Поиск по ID
@dp.callback_query_handler(text="search_id")
async def search_date(callback: CallbackQuery, state=FSMContext):
    await callback.message.edit_text(text="Введите адрес:")
    await state.set_state(Incidents.incident_search_id)


# 5.1 Ввод ID
@dp.message_handler(state=Incidents.incident_search_id)
async def search_date_insert(message: types.Message, state=FSMContext):
    if message.text.isdigit() == True:
        logs_infomation = [message.from_user.username, message.from_user.id, "story_search_id", message.text]
        lg.logs(data_dict=logs_infomation, action="incidents")

        result_search = search.search_in_base(data=int(message.text), mode="id")
        if result_search:
            for item in result_search:
                await bot.send_message(message.from_user.id, f"ID: {item[0]}\nРаскрыто: {item[1]}\nДата совершения: {item[2]}\nАдрес: {item[3]}\nСотрудник: {item[4]}\nФабула: {item[5]}")
            await state.finish()
            await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "По указанному ID информации не обнаружено.\n\nВыберите необходимую функцию:", reply_markup=nav.inline_reply_button)

    else:
        await bot.send_message(message.from_user.id, "ID введен не корректно.\n Введите еще раз:")        


# 6.1 Вывод все эпизодов
@dp.callback_query_handler(text="all_incidents")
async def search_all_incidents(callback: CallbackQuery, state=FSMContext):
    result_search = search.search_in_base_revelation(mode="all")
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    from_req.form_story_in_html(db_list=result_search, search_title="Все преступления", userid=callback.from_user.id, mode="default")
    await bot.send_document(callback.from_user.id, open(f"user_files/Все преступления_{callback.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
    await state.finish()
    await bot.send_message(callback.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)




# 1     Кнопка просмотра всех эпизодов  (+) search_db.py
# 1.1   Сортировка по раскрытым         (+) search_db.py
# 1.2   Сортировка по не раскрытым      (+) search_db.py
# 1.3   Посик по дате                   (+) search_db.py
# 1.4   Поиск по адресу                 (+) search_db.py


# Карточка: 1. Порядковый номер, 2. Раскрытие,      (+) 
# 3. Дата совершения, 4. Адрес совершения,           |  insert_in_base.py
# 5. Кто выезжал, 6. Фабула                         (+) 

# 1. Добавление фотографий, 2. Формирование отчета в HTML-файл,         (-)
# 3. Логирование поиска, 4. Добавление в базу дату введения информации  (-)

# Карточка заносится в SQL-таблицу.     (+) insert_in_base.py

# 2     Кнопка добавления новых эпизодов    (+)
# 2.1   Введите кто выезжал                  |
# 2.2   Введите дату                         |  add_new_story.py
# 2.3   Ведите адрес                         |
# 2.4   Введите фабулу                      (+)