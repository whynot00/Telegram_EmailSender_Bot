from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram import types

# Кнопки главного меню (/start)

# Реплай-кнопки

main_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_button_1 = KeyboardButton("Отмена")

main_button_send = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_button_2 = KeyboardButton("Отправить")

main_button_send.add(main_button_2).add(main_button_1)
main_button.add(main_button_1)

# Инлайн-кнопки 

inline_reply_button = types.InlineKeyboardMarkup()
inline_reply_button_1 = types.InlineKeyboardButton(text="Отправить файлы", callback_data="send_files")
inline_reply_button_2 = types.InlineKeyboardButton(text="add_incident", callback_data="add_incident")
inline_reply_button.add(inline_reply_button_1).add(inline_reply_button_2)


##########################################################################


# Кноки добавления пользователя (/add_member)

# Инлайн-кнопки


inline_reply_members_btn1 = types.InlineKeyboardButton(text="Добавить пользователя", callback_data="add_member")
inline_reply_members_btn2 = types.InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_member")
inline_reply_members = types.InlineKeyboardMarkup().row(inline_reply_members_btn1, inline_reply_members_btn2)

inline_reply_add_mem_btn1 = types.InlineKeyboardButton(text="Администратор", callback_data="add_member")
inline_reply_add_mem_btn2 = types.InlineKeyboardButton(text="Пользователь", callback_data="delete_member")
inline_reply_addmem = types.InlineKeyboardMarkup().add(inline_reply_add_mem_btn1).add(inline_reply_add_mem_btn2)

