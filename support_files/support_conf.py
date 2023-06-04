from aiogram import types
from support_files import buttons as nav


user_id_for_send: set[int] = set()

    # Костыль для ответа группе файлов
async def user_send_conf(user: types.User):
    if user.id in user_id_for_send:
        return

    user_id_for_send.add(user.id)
    # await bot.send_message(user.id, "Файлы готовы к отправке", reply_markup=nav.main_button_send)
    return True

