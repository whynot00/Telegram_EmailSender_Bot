from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from misc import dispatcher as dp
from misc import bot

from support_files import buttons as nav
from support_files import whitelist_checker as wl_check
from support_files.incidents import insert_in_base as base
from support_files.incidents import search_db as search


class Reference(StatesGroup):
    organization = State()


@dp.callback_query_handler(text="reference")
async def reference_menu(callback: CallbackQuery):
    if wl_check.whitelist_checker(callback.from_user.id, powers="users") != True:
        return
    
    await callback.message.edit_text(text="Выберите справку", reply_markup=nav.inline_reply_reference)



@dp.callback_query_handler(text="organization")
async def reference_organization(callback: CallbackQuery, state=FSMContext):
    await state.set_state(Reference.organization)
    await callback.message.edit_text(text="Введите наименование организации:")

@dp.message_handler(state=Reference.organization)
async def insert_organization(message: types.Message, state=FSMContext):
    result_search = search.search_in_base(data=message.text.lower(), mode="reference")
    if result_search:
        for item in result_search:
            await bot.send_message(message.from_user.id, text=f"<b>Бренд:</b> {item[2]}\n<b>Юр. лицо:</b> {item[3]}\n<b>ФИО:</b> {item[4]}\n<b>Должность:</b> {item[5]}\n<b>Телефон:</b> {item[6]}\n<b>E-mail:</b> {item[7]}\n<b>Коментарий:</b> {item[8]}\n")
        await bot.send_message(message.from_user.id, text="Главное меню:", reply_markup=nav.general_menu_inline)
    else:
        await bot.send_message(message.from_user.id, text="По данному запросу информации нет.\n\nГлавное меню:", reply_markup=nav.general_menu_inline)

    await state.finish()
