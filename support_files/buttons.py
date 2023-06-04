from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram import types

main_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_button_1 = KeyboardButton("Upload a file")
main_button_2 = KeyboardButton("Cancel")

main_button_send = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_button_3 = KeyboardButton("Send")

main_button_send.add(main_button_3).add(main_button_2)
main_button.add(main_button_2)

##########################################################################


inline_reply_button = types.InlineKeyboardMarkup()
inline_reply_button_1 = types.InlineKeyboardButton(text="Send files", callback_data="send_files")
# inline_reply_button_2 = types.InlineKeyboardButton(text="Group Search", callback_data="find_group")
inline_reply_button.add(inline_reply_button_1).add(inline_reply_button_2)

