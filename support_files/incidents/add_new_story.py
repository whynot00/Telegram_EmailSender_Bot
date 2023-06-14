from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from datetime import datetime

import os

from misc import dispatcher as dp
from misc import bot

from support_files import buttons as nav
from support_files import send_email
from support_files import logs as lg
from support_files import whitelist_checker as wl_check
from support_files.incidents import insert_in_base as base
from support_files.incidents import search_db as search
from support_files.incidents import normal_address as normalize

class Incidents(StatesGroup):
    incident = State()
    incident_add_new_story_1 = State()
    incident_add_new_story_2 = State()
    incident_add_new_story_3 = State()
    incident_add_new_story_4 = State()
    incident_add_new_story_5 = State()
    incident_add_new_story_6 = State()


# Реакция на выход с отправки /// хз как работает на нескольких этапах????
@dp.message_handler(text=nav.main_button_1.text, state=[Incidents.incident, Incidents.incident_add_new_story_1, Incidents.incident_add_new_story_2, Incidents.incident_add_new_story_3, Incidents.incident_add_new_story_4, Incidents.incident_add_new_story_5])
async def poyti_nahooi(message: types.Message, state=FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Выход в галвное меню.", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button) 


# 1.1 Вход в добавление инцидента
@dp.callback_query_handler(text="add_new_incident")
async def add_new_story(callback: CallbackQuery, state=FSMContext):
    if wl_check.whitelist_checker(user_id=callback.from_user.id, powers="admin") != True:
        await bot.send_message(callback.from_user.id, "У вас недостаточно прав.", reply_markup=nav.inline_reply_button)
        return

    await bot.send_message(callback.from_user.id, "Введите дату соврешения преступления.", reply_markup=nav.main_button)
    await state.set_state(Incidents.incident_add_new_story_1)


# 1.2 Ввод даты
@dp.message_handler(state=Incidents.incident_add_new_story_1)
async def insert_date_story(message: types.Message, state=FSMContext): 
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y')
        async with state.proxy() as data:
            data["date_story"] = str(message.text)
        await state.set_state(Incidents.incident_add_new_story_2)
        await bot.send_message(message.from_user.id, "Введите адрес совершения преступления:", reply_markup=nav.main_button)

    except ValueError:
        await bot.send_message(message.from_user.id, "Дата введена некоректно.\n\nВведите снова:", reply_markup=nav.main_button)


# 1.3 Ввод адреса
@dp.message_handler(state=Incidents.incident_add_new_story_2)
async def insert_address_story(message: types.Message, state=FSMContext):
    result_normalize = normalize.normalize_address(message.text)
    if normalize.adress_check_true(result_normalize) == True:
        async with state.proxy() as data:
            data["address_story"] = result_normalize
        
        await bot.send_message(message.from_user.id, "Введите сотрудника, кто выезжал от УУР:", reply_markup=nav.main_button)
        await state.set_state(Incidents.incident_add_new_story_3)
    else:
        await bot.send_message(message.from_user.id, "Адрес введен некорректно (не соотвествует карте)\nВведите снова:", reply_markup=nav.main_button)

# 1.4 Ввод сотрудника
@dp.message_handler(state=Incidents.incident_add_new_story_3)
async def insert_fellow_story(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["fellow_story"] = message.text.title()
    await state.set_state(Incidents.incident_add_new_story_4)

    await bot.send_message(message.from_user.id, "Преступление раскрыто?\n\nДа\\Нет", reply_markup=nav.main_button)


# 1.5 Ввод раскрытия
@dp.message_handler(state=Incidents.incident_add_new_story_4)
async def insert_revelation_story(message: types.Message, state=FSMContext):
    if ("да" in message.text.lower() or "нет" in message.text.lower()):
        async with state.proxy() as data:
            data["revelation_story"] = message.text.title()
        await state.set_state(Incidents.incident_add_new_story_5)
        await bot.send_message(message.from_user.id, "Введите тип преступления:\n ДТП\\Банк", reply_markup=nav.main_button)
    else:
        await bot.send_message(message.from_user.id, "Раскрытие введено не верно.\nВведите еща раз (Да\\Нет):", reply_markup=nav.main_button)

# 1.6 Ввод типа преступления
@dp.message_handler(state=Incidents.incident_add_new_story_5)
async def insert_text_story(message: types.Message, state=FSMContext):
    
    async with state.proxy() as data:
        if (message.text.lower() == "дтп" or message.text.lower() == "банк"):
            data["crime_type"] = message.text
            await state.set_state(Incidents.incident_add_new_story_6)
            await bot.send_message(message.from_user.id, "Введите фабулу преступления:")
        
        else:
            await bot.send_message(message.from_user.id, "Некоректный ввод.\n\nВведите снова:\nДТП\\Банк")


# 1.7 Ввод фабулы
@dp.message_handler(state=Incidents.incident_add_new_story_6)
async def insert_text_story(message: types.Message, state=FSMContext):
    
    async with state.proxy() as data:
        data["story"] = message.text
    result_add = f'Раскрыто: {data["revelation_story"]}\nВид преступления: {data["crime_type"]}\nДата совершения: {data["date_story"]}\nАдрес: {data["address_story"]}\nСотрудник: {data["fellow_story"]}\nФабула: {data["story"]}'

    await bot.send_message(message.from_user.id, f"Подвтердите верность данных:\n\n{result_add}", reply_markup=nav.inline_reply_incident_confirm_story)


# 1.8 Ввод фотографии
@dp.callback_query_handler(text="add_photo_incident", state=Incidents.incident_add_new_story_6)
async def add_photo_incident(callback: CallbackQuery, state=FSMContext):
    await callback.message.edit_text(text="Данная функиция пока не работает", reply_markup=nav.inline_reply_incident_confirm_story)


# 1.9 Подтверждение
@dp.callback_query_handler(text="confirm_add_incident", state=Incidents.incident_add_new_story_6)
async def confirm_add_incident(callback: CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        result_add = [data["revelation_story"], data["date_story"], data["address_story"], data["fellow_story"], data["story"], data["crime_type"]]

    logs_infomation = [callback.from_user.username, callback.from_user.id, "story_add_story", "stories"]
    lg.logs(data_dict=logs_infomation, action="incidents")
    base.insert_story(result_add)

    await state.finish()
    await callback.message.edit_text(text="Карточка внесена!\n\nГлавное меню.", reply_markup=nav.inline_reply_button)