from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram import types

main_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_button_1 = KeyboardButton("Скинуть файл")
main_button_2 = KeyboardButton("Отмена")

main_button_send = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_button_3 = KeyboardButton("Отправить")

main_button_send.add(main_button_3).add(main_button_2)
main_button.add(main_button_2)

##########################################################################


inline_reply_button = types.InlineKeyboardMarkup()
inline_reply_button_1 = types.InlineKeyboardButton(text="Отправить файлы", callback_data="send_files")
inline_reply_button_2 = types.InlineKeyboardButton(text="Поиск по группам", callback_data="find_group")
inline_reply_button.add(inline_reply_button_1).add(inline_reply_button_2)

