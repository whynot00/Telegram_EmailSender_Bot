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
    incident_search_id_add_1 = State()
    incident_search_id_add_2 = State()
    incident_search_id_photos = State()


# Реакция на вход в инциденты
@dp.callback_query_handler(text="incidents")
async def incident_info(callback: CallbackQuery, state=FSMContext):
    await callback.answer()
    if wl_check.whitelist_checker(callback.from_user.id, powers="users") != True:
        return

    await callback.message.edit_text(text="<b>Поиск по эпизодам</b>:", reply_markup=nav.inline_reply_incident)


# 1 Inline-кнопки
@dp.callback_query_handler(text=["search_geo", "search_date", "search_address", "search_id"])
async def incident_form_exp(callback: CallbackQuery, state=FSMContext):
    await callback.answer()
    # 1.1 Поиск по дате
    if callback.data == "search_date":
        await callback.message.edit_text(text="<b>Поиск.</b>")
        await bot.send_message(callback.from_user.id, "Введите дату:", reply_markup=nav.cancel_key_button)
        await state.set_state(Incidents.incident_search_date)

    # 1.2 Поиск по адресу
    elif callback.data == "search_address":
        await callback.message.edit_text(text="<b>Поиск.</b>")
        await bot.send_message(callback.from_user.id, "Введите адрес:", reply_markup=nav.cancel_key_button)
        await state.set_state(Incidents.incident_search_address)

    # 1.3 Поиск по ID
    elif callback.data == "search_id":
        await callback.message.edit_text(text="<b>Поиск.</b>")
        await bot.send_message(callback.from_user.id, "Введите ID:", reply_markup=nav.cancel_key_button)
        await state.set_state(Incidents.incident_search_id)

    # 1.4 Поиск по геолокации
    elif callback.data == "search_geo":
        await callback.message.edit_text(text="<b>Отправьте необходимую геолокацию:</b>", reply_markup=nav.cancel_button)
        await state.set_state(Incidents.incident_search_geo)


# 2 Ввод данных
@dp.message_handler(content_types=['any'],state=[Incidents.incident_search_date, Incidents.incident_search_address ,Incidents.incident_search_id, Incidents.incident_search_geo])
async def search_date_insert(message: types.Message, state=FSMContext):
    get_state = await state.get_state()

    # 2.1 Ввод даты
    if get_state == "Incidents:incident_search_date":
        try:
            date = datetime.strptime(message.text, '%d.%m.%Y')
            result_search = search.search_in_base(data=message.text, mode="date")
            if result_search: 
                if len(result_search) <= 2:
                    for item in result_search:
                        await bot.send_message(message.from_user.id, f"<b>ID:</b> {item[0]}\n<b>КУСП:</b> {item[8]}\n<b>Вид преступления:</b> {item[6]}\n<b>Раскрытие:</b> {item[1]}\n<b>Дата совершения:</b> {item[2]}\n<b>Адрес:</b> {item[3]}\n<b>Сотрудник:</b> {item[4]}\n<b>Сотрудник:</b> {item[12]}\n<b>Дата задержания:</b> {item[13]}\n<b>Статус:</b> {item[14]}\n<b>ID телеграм-аккаунта:</b> {item[15]}\n<b>Номер уголовного дела:</b> {item[9]} от {item[10]}\n<b>Статья УК:</b> {item[11]}\n<b>Фабула:</b> {item[5]}")
                    await state.finish()
                    await bot.send_message(message.from_user.id, "Главное меню:", reply_markup=nav.general_menu_inline)
                else:
                    from_req.form_story_in_html(db_list=result_search, search_title="Поиск по дате", userid=message.from_user.id, mode="default")
                    await bot.send_document(message.from_user.id, open(f"user_files/Поиск по дате_{message.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
                    await bot.send_message(message.from_user.id, "Главное меню:", reply_markup=nav.general_menu_inline)
                    os.unlink(f"user_files/Поиск по дате_{str(message.from_user.id)}.html")
                    await state.finish()
            else:
                await state.finish()
                await bot.send_message(message.from_user.id, f"<b>За данную дату преступлений не происходило.</b>\n\nГлавное меню:", reply_markup=nav.general_menu_inline)
            
            logs_infomation = [message.from_user.username, message.from_user.id, "story_search_date", message.text]
        except ValueError:
            await bot.send_message(message.from_user.id, "Дата введена некоректно.\n\nВведите снова:", reply_markup=nav.general_menu_inline)
    
    # 2.2 Ввод адреса
    elif get_state == "Incidents:incident_search_address":
        result_search = search.search_in_base(data=normalize.normalize_address(message.text), mode="address")
        if result_search:
            if len(result_search) <= 2:
                for item in result_search:
                    await bot.send_message(message.from_user.id, f"<b>ID:</b> {item[0]}\n<b>КУСП:</b> {item[8]}\n<b>Вид преступления:</b> {item[6]}\n<b>Раскрытие:</b> {item[1]}\n<b>Дата совершения:</b> {item[2]}\n<b>Адрес:</b> {item[3]}\n<b>Сотрудник:</b> {item[4]}\n<b>Сотрудник:</b> {item[12]}\n<b>Дата задержания:</b> {item[13]}\n<b>Статус:</b> {item[14]}\n<b>ID телеграм-аккаунта:</b> {item[15]}\n<b>Номер уголовного дела:</b> {item[9]} от {item[10]}\n<b>Статья УК:</b> {item[11]}\n<b>Фабула:</b> {item[5]}")
                await state.finish()
                await bot.send_message(message.from_user.id, "Главное меню:", reply_markup=nav.general_menu_inline)
            else:
                from_req.form_story_in_html(db_list=result_search, search_title="Поиск по адресу", userid=message.from_user.id, mode="default")
                await bot.send_document(message.from_user.id, open(f"user_files/Поиск по адресу_{message.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
                await bot.send_message(message.from_user.id, "Главное меню.", reply_markup=nav.general_menu_inline)
                os.unlink(f"user_files/Поиск по адресу_{str(message.from_user.id)}.html")
                await state.finish()
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "</b>По указанному адресу преступлений не происходило.</b>\n\nГлавное меню:", reply_markup=nav.general_menu_inline)
        
        logs_infomation = [message.from_user.username, message.from_user.id, "story_search_address", message.text]

    # 2.3 Ввод ID
    elif get_state == "Incidents:incident_search_id":
        if message.text.isdigit() == True:
            result_search = search.search_in_base(data=int(message.text), mode="id")
            if result_search == False:
                await bot.send_message(message.from_user.id, "Информации по данному ID нет.\n\nГлавное меню:", reply_markup=nav.general_menu_inline)
                await state.finish()
                return
            from_req.form_story_in_html(db_list=result_search, search_title="Поиск по ID", userid=message.from_user.id, mode="ID")

            await bot.send_document(message.from_user.id, open(f"user_files/Поиск по ID_{message.from_user.id}.html", "rb"), caption="Полный отчет о эпизоде.")
            if wl_check.whitelist_checker(user_id=message.from_user.id, powers="moderator") == True:
                async with state.proxy() as data:
                    data["id_incident"] = message.text
                await bot.send_message(message.from_user.id, "Соотнести лицо:", reply_markup=nav.insert_id_criminal)
            else: 
                await bot.send_message(message.from_user.id, "Главное меню:", reply_markup=nav.general_menu_inline)
                os.unlink(f"user_files/Поиск по ID_{str(message.from_user.id)}.html")
                await state.finish()
        else:
            await bot.send_message(message.from_user.id, "ID введен не корректно.\n Введите еще раз:")

        logs_infomation = [message.from_user.username, message.from_user.id, "story_search_id", message.text]
    
    lg.logs(data_dict=logs_infomation, action="incidents")
    

# 3 Вывод данных 
@dp.callback_query_handler(text=["sort_rev_yes", "sort_rev_none", "all_incidents"])
async def sort_any(callback: CallbackQuery, state=FSMContext):
    await callback.answer()

    # 3.1 Вывод раскрытых
    if callback.data == "sort_rev_yes":
        result_search = search.search_in_base_revelation(mode="Да")
        if len(result_search) <= 2:
            for item in result_search:
                await bot.send_message(callback.from_user.id, f"<b>ID:</b> {item[0]}\n<b>Раскрыто:</b> {item[1]}\n<b>Дата совершения:</b> {item[2]}\n<b>Адрес:</b> {item[3]}\n<b>Сотрудник:</b> {item[4]}\n<b>Фабула:</b> {item[5]}")
            await bot.send_message(callback.from_user.id, "Главное меню:", reply_markup=nav.general_menu_inline)
        else:
            from_req.form_story_in_html(db_list=result_search, search_title="Раскрытые преступления", userid=callback.from_user.id, mode="default")
            await bot.send_document(callback.from_user.id, open(f"user_files/Раскрытые преступления_{callback.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
            await bot.send_message(callback.from_user.id, "Главное меню.", reply_markup=nav.general_menu_inline)
            os.unlink(f"user_files/Раскрытые преступления_{str(callback.from_user.id)}.html")

        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        logs_infomation = [callback.from_user.username, callback.from_user.id, "story_sort_revelation", "yes"]
        
    # 3.1 Вывод нераскрытых
    elif callback.data == "sort_rev_none":
        result_search = search.search_in_base_revelation(mode="Нет")
        if len(result_search) <= 2:
            for item in result_search:
                await bot.send_message(callback.from_user.id, f"<b>ID:</b> {item[0]}\n<b>Раскрыто:</b> {item[1]}\n<b>Дата совершения:</b> {item[2]}\n<b>Адрес:</b> {item[3]}\n<b>Сотрудник:</b> {item[4]}\n<b>Фабула:</b> {item[5]}")
            await bot.send_message(callback.from_user.id, "Главное меню:", reply_markup=nav.general_menu_inline)
        else:
            from_req.form_story_in_html(db_list=result_search, search_title="Нераскрытые преступления", userid=callback.from_user.id, mode="default")
            await bot.send_document(callback.from_user.id, open(f"user_files/Нераскрытые преступления_{callback.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
            await bot.send_message(callback.from_user.id, "Главное меню.", reply_markup=nav.general_menu_inline)
            os.unlink(f"user_files/Нераскрытые преступления_{str(callback.from_user.id)}.html")

        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        logs_infomation = [callback.from_user.username, callback.from_user.id, "story_sort_revelation", "none"]

    # 3.1 Вывод всех эпизодов
    elif callback.data == "all_incidents":
        result_search = search.search_in_base_revelation(mode="all")
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        from_req.form_story_in_html(db_list=result_search, search_title="Все преступления", userid=callback.from_user.id, mode="default")
        await bot.send_document(callback.from_user.id, open(f"user_files/Все преступления_{callback.from_user.id}.html", "rb"), caption="В сводке более двух эпизодов, сформирован отчетный файл.")
        await bot.send_message(callback.from_user.id, "Главное меню:", reply_markup=nav.general_menu_inline)
        os.unlink(f"user_files/Все преступления_{str(callback.from_user.id)}.html")
        
        logs_infomation = [callback.from_user.username, callback.from_user.id, "story_sort_all_incidents", "all_inicdents"]

    lg.logs(data_dict=logs_infomation, action="incidents")


@dp.callback_query_handler(text="add_id_criminal", state=Incidents.incident_search_id)
async def add_id_criminal_inc(callback: CallbackQuery, state=FSMContext):
    await callback.answer()
    await callback.message.edit_text("<b>Введите ФИО лица:</b>")
    await state.set_state(Incidents.incident_search_id_add_1)

@dp.message_handler(state=[Incidents.incident_search_id_add_1, Incidents.incident_search_id_add_2])
async def add_id_criminal_inc_insert(message: types.Message, state=FSMContext):
    get_state = await state.get_state()

    if get_state == "Incidents:incident_search_id_add_1":
        result_search, message_result = search.search_in_base(data=message.text, mode="criminals")
        print(result_search[0][-7])
        if not result_search:
            await bot.send_message(message.from_user.id, "<b>По запрошеным данным, информации нет.\n\nГлавное меню:</b>", reply_markup=nav.general_menu_inline)
            await state.finish()
        
        elif message_result is None:
            async with state.proxy() as data:
                id_incident = data["id_incident"]
            base.update_id(id_incident=id_incident, id_criminal=result_search[0][-7])
            await bot.send_message(message.from_user.id, "<b>Эпизод и лицо успешно соотнесено!</b>\n\nГлавное меню:", reply_markup=nav.general_menu_inline)
            await state.finish()

        else:
            await bot.send_message(message.from_user.id, message_result)
            await state.set_state(Incidents.incident_search_id_add_2)

    if get_state == "Incidents:incident_search_id_add_2":
        async with state.proxy() as data:
            id_incident = data["id_incident"]
        base.update_id(id_incident=id_incident, id_criminal=message.text)
        await bot.send_message(message.from_user.id, "<b>Эпизод и лицо успешно соотнесено!</b>\n\nГлавное меню:", reply_markup=nav.general_menu_inline)
        await state.finish()


# 1     Кнопка просмотра всех эпизодов  (+) search_db.py
# 1.1   Сортировка по раскрытым         (+) search_db.py
# 1.2   Сортировка по не раскрытым      (+) search_db.py
# 1.3   Посик по дате                   (+) search_db.py
# 1.4   Поиск по адресу                 (+) search_db.py


# Карточка: 1. Порядковый номер, 2. Раскрытие,      (+) 
# 3. Дата совершения, 4. Адрес совершения,           |  insert_in_base.py
# 5. Кто выезжал, 6. Фабула                         (+) 

# 1. Добавление фотографий, 2. Формирование отчета в HTML-файл(+),         (+-)
# 3. Логирование поиска(+), 4. Добавление в базу дату введения информации  (+-)

# Карточка заносится в SQL-таблицу.     (+) insert_in_base.py

# 2     Кнопка добавления новых эпизодов    (+)
# 2.1   Введите кто выезжал                  |
# 2.2   Введите дату                         |  add_new_story.py
# 2.3   Ведите адрес                         |
# 2.4   Введите фабулу                      (+)

# 3     Задержанные лица                                        (-)
# 3.1   ФИО                                                      |
# 3.2   Год рождения                                             |
# 3.3   Фотографии                                               |
# 3.4   Статус (подозреваемый, обвиняемый, в рот выебанный)      |
# 3.5   Эпизоды за ним (заявленные указание по ID)              (-)
# 3.6   Когда задержан