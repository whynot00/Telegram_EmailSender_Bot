from misc import dispatcher as dp
from misc import bot
from aiogram.dispatcher import FSMContext
from aiogram import types

from support_files import buttons as nav
from support_files import whitelist_checker as wl_check


    # Команда старт, которая обращается к навигационному меню
@dp.message_handler(commands="start")
async def start(message: types.Message):
    if wl_check.whitelist_checker(str(message.from_user.id), powers="users") != True:
        return
    wl_check.check_username(str(message.from_user.id), message.from_user.username)
    
    await bot.send_message(message.from_user.id, "<b>Информационная система ОМТ</b>\n\nГлавное меню:", reply_markup=nav.general_menu_inline)
