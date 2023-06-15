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
inline_reply_button_1 = types.InlineKeyboardButton(text="Почта", callback_data="send_files")
inline_reply_button_2 = types.InlineKeyboardButton(text="Преступления", callback_data="incidents")
inline_reply_button_3 = types.InlineKeyboardButton(text="Справка", callback_data="reference")
inline_reply_button.row(inline_reply_button_1, inline_reply_button_2).add(inline_reply_button_3)


##########################################################################


# Кноки добавления пользователя (/add_member)

# Инлайн-кнопки


inline_reply_members_btn1 = types.InlineKeyboardButton(text="Добавить пользователя", callback_data="add_member")
inline_reply_members_btn2 = types.InlineKeyboardButton(text="Удалить пользователя", callback_data="delete_member")
inline_reply_members = types.InlineKeyboardMarkup().row(inline_reply_members_btn1, inline_reply_members_btn2)

inline_reply_add_mem_btn1 = types.InlineKeyboardButton(text="Администратор", callback_data="admin_btn")
inline_reply_add_mem_btn2 = types.InlineKeyboardButton(text="Пользователь", callback_data="user_btn")
inline_reply_addmem = types.InlineKeyboardMarkup().add(inline_reply_add_mem_btn1).add(inline_reply_add_mem_btn2)

inline_reply_add = types.InlineKeyboardButton(text="Добавить", callback_data="add_btn")
inline_reply_add_btn = types.InlineKeyboardMarkup().add(inline_reply_add)

delete_btn = KeyboardButton("Удалить")
delete_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(delete_btn).add(main_button_1)

add_btn = KeyboardButton("Добавить")
add_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(add_btn).add(main_button_1)


##########################################################################

# Кнопки инцидентов

# Инлайн-кнопки

inline_reply_incident_btn1 = types.InlineKeyboardButton(text="Все эпизоды", callback_data="all_incidents")
inline_reply_incident_btn2 = types.InlineKeyboardButton(text="Поиск по дате", callback_data="search_date")
inline_reply_incident_btn3 = types.InlineKeyboardButton(text="Поиск по адресу", callback_data="search_address")
inline_reply_incident_btn10 = types.InlineKeyboardMarkup(text="Поиск по геолокации", callback_data="search_geo")
inline_reply_incident_btn4 = types.InlineKeyboardButton(text="Раскрытые", callback_data="sort_rev_yes")
inline_reply_incident_btn5 = types.InlineKeyboardButton(text="Не раскрытые", callback_data="sort_rev_none")
inline_reply_incident_btn6 = types.InlineKeyboardButton(text="Внести эпизод", callback_data="add_new_incident")
inline_reply_incident_btn9 = types.InlineKeyboardButton(text="Поиск ID", callback_data="search_id")

inline_reply_incident_btn7 = types.InlineKeyboardButton(text="Добавить фотографию", callback_data="add_photo_incident")
inline_reply_incident_btn8 = types.InlineKeyboardButton(text="Завершить", callback_data="confirm_add_incident")


inline_reply_incident = types.InlineKeyboardMarkup().row(inline_reply_incident_btn1, inline_reply_incident_btn9).row(inline_reply_incident_btn2, inline_reply_incident_btn3).add(inline_reply_incident_btn10)
inline_reply_incident.row(inline_reply_incident_btn4, inline_reply_incident_btn5).add(inline_reply_incident_btn6)

inline_reply_incident_confirm_story = types.InlineKeyboardMarkup().row(inline_reply_incident_btn7, inline_reply_incident_btn8)


##########################################################################

# Кнопки справки

inline_reply_reference_btn1 = types.InlineKeyboardButton(text="Организации", callback_data="organization")
inline_reply_reference_btn2 = types.InlineKeyboardButton(text="inline", callback_data="inline")

inline_reply_reference = types.InlineKeyboardMarkup().row(inline_reply_reference_btn1, inline_reply_reference_btn2)