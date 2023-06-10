from misc import dispatcher as dp
from misc import bot
from aiogram.dispatcher import FSMContext
from aiogram import types

from support_files import buttons as nav
from support_files import whitelist_checker as wl_check


    # Команда старт, которая обращается к навигационному меню
@dp.message_handler(commands="start")
async def start(message: types.Message):
    check = wl_check.whitelist_checker(message.from_user.id, powers="users")
    print(check)
    if check != True:
        return
    await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)
