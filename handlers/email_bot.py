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
from support_files import logs as lg
from support_files import send_email
from support_files import whitelist_checker as wl_check


class Form(StatesGroup):
    recipients = State()
    button_send = State()


   # Реакция на выход с отправки /// хз как работает на нескольких этапах????
@dp.message_handler(text=nav.main_button_1.text, state="*")
async def poyti_nahooi(message: types.Message, state=Form.button_send):
    await state.finish()
    await bot.send_message(message.from_user.id, "Выход в галвное меню.", reply_markup=types.ReplyKeyboardRemove())
    if os.path.exists(f"user_files/{message.from_user.id}") == True:
        shutil.rmtree(f"user_files/{str(message.from_user.id)}")
    if message.from_user.id in support.user_id_for_send:
        support.user_id_for_send.remove(message.from_user.id)
    await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button) 


    # Ответ на inline-кнопку
@dp.callback_query_handler(text="send_files")
async def send_files_button(message: types.Message, state=FSMContext):
    if wl_check.whitelist_checker(message.from_user.id, powers="users") == True:
        await state.set_state(Form.recipients)
        await bot.send_message(message.from_user.id,"Напишите фамилию получателя:", reply_markup=nav.main_button)

    # Ввод получателя
@dp.message_handler(state=Form.recipients)
async def recipients(message: types.Message, state=FSMContext):
    with open("configurations/recipients.json", "r", encoding="utf-8") as file:
        recipients_dict = json.load(file)
        if message.text.lower() in recipients_dict:
            await bot.send_message(message.from_user.id, "Отправте файл/файлы:", reply_markup=nav.main_button)
            async with state.proxy() as data:
                data["recipient"] = recipients_dict[message.text.lower()]
            await Form.next()
        else:
            await bot.send_message(message.from_user.id, "Такого пользователя не существует.", reply_markup=nav.main_button)


    # Реакция на получение файла, скачитвается в папку "user_files", где так же сохраняется в папку с названием id пользователя
@dp.message_handler(content_types=(['document', 'photo']), state=Form.button_send)
async def documents(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if message.content_type == "document":
            file_info = await bot.get_file(message.document.file_id)
            await message.document.download(f"user_files/{str(message.from_user.id) + file_info.file_path.replace('documents', '')}")
            data["type"] = "documement"
        elif message.content_type == "photo":
            file_info = await bot.get_file(message.photo[-1].file_id)
            await message.photo[-1].download(f"user_files/{str(message.from_user.id) + file_info.file_path.replace('photos', '')}")
            data["type"] = "photo"
        else:
            return
    if await support.user_send_conf(message.from_user) == True:
        await bot.send_message(message.from_user.id, "Файлы готовы к отправке", reply_markup=nav.main_button_send)
    


    # Реакция на нажатие кнопки отправки
@dp.message_handler(text=nav.main_button_2.text, state=Form.button_send)
async def send_button(message: types.Message, state=FSMContext):
    sender_info_dict = {
        "user_id": message.from_user.id,
        "user_username": message.from_user.username,
    }
    async with state.proxy() as data:
        sender_info_dict["recipient"] = data["recipient"]
        sender_info_dict["type"] = data["type"]
    send_email.main(sender_info_dict)
    await bot.send_message(message.from_user.id, "Файлы успешно отправлены.", reply_markup=types.ReplyKeyboardRemove())
    shutil.rmtree(f"user_files/{str(sender_info_dict['user_id'])}")
    
    logs_infomation = [sender_info_dict["user_username"], sender_info_dict["user_id"], sender_info_dict["recipient"], sender_info_dict["type"]]
    lg.logs(data_dict=logs_infomation, action="email_send")

    await state.finish()
    await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
    support.user_id_for_send.remove(message.from_user.id)


    # Реакция на неправильный ввод команды(miss_buttons)
@dp.message_handler(state=Form.button_send)
async def invalid_message(message: types.Message, state=FSMContext):
    await bot.send_message(message.from_user.id, "Используйте кнопки снизу.", reply_markup=nav.main_button)