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



@dp.callback_query_handler(text="cancel", state="*")
async def cancel_def(callback: CallbackQuery, state=FSMContext):
    await callback.answer()
    await state.finish()
    await callback.message.edit_text("<b>Отмена.</b>\nГлавное меню:", reply_markup=nav.general_menu_inline)


@dp.callback_query_handler(text="general_search")
async def general_search(callback: CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text="<b>Выберите функцию:</b>", reply_markup=nav.search_menu_inline)

@dp.callback_query_handler(text="general_insert")
async def general_search(callback: CallbackQuery):
    await callback.answer()
    await bot.send_message(callback.from_user.id, text="<b>Выберите функцию:</b>", reply_markup=nav.incert_menu_inline)
