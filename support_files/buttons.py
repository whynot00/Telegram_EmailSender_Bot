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
inline_reply_button_4 = types.InlineKeyboardButton(text="Лица", callback_data="crimes")
inline_reply_button_5 = types.InlineKeyboardButton(text="Уголовыне дела", callback_data="case")
inline_reply_button.row(inline_reply_button_1, inline_reply_button_2).row(inline_reply_button_3, inline_reply_button_4).add(inline_reply_button_5)


##########################################################################


# Кноки добавления пользователя (/add_member)

# Инлайн-кнопки


inline_reply_members_btn1 = types.InlineKeyboardButton(text="Добавить", callback_data="add_member")
inline_reply_members_btn2 = types.InlineKeyboardButton(text="Удалить", callback_data="delete_member")
inline_reply_members = types.InlineKeyboardMarkup().row(inline_reply_members_btn1, inline_reply_members_btn2)

inline_reply_add_mem_btn1 = types.InlineKeyboardButton(text="Модератор", callback_data="moder_btn")
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
inline_reply_incident_btn9 = types.InlineKeyboardButton(text="Поиск ID", callback_data="search_id")

inline_reply_incident_btn7 = types.InlineKeyboardButton(text="Добавить фотографию", callback_data="add_photo_incident")
inline_reply_incident_btn8 = types.InlineKeyboardButton(text="Завершить", callback_data="confirm_add_incident")


inline_reply_incident_confirm_story = types.InlineKeyboardMarkup().row(inline_reply_incident_btn7, inline_reply_incident_btn8)

inline_reply_incident_addphoto = types.InlineKeyboardMarkup().add(inline_reply_incident_btn7)

##########################################################################

# Кнопки справки

inline_reply_reference_btn1 = types.InlineKeyboardButton(text="Организации", callback_data="organization")
inline_reply_reference_btn2 = types.InlineKeyboardButton(text="inline", callback_data="inline")



inline_reply_crimes_btn1 = types.InlineKeyboardButton(text="Поиск по ФИО", callback_data="search_crimes_name")
inline_reply_crimes_btn3 = types.InlineKeyboardButton(text="Все лица", callback_data="all_crimes")

# inline_reply_crimes_names = types.InlineKeyboardMarkup().add(inline_reply_crimes_btn3).row(inline_reply_crimes_btn1, inline_reply_crimes_btn2)

##########################################################################

# Кнопки уголовных дел


inline_reply_case_btn2 = types.InlineKeyboardButton(text="Поиск", callback_data="search_case")

# inline_reply_case = types.InlineKeyboardMarkup().row(inline_reply_case_btn1, inline_reply_case_btn2)

##########################################################################

cancel_button = types.InlineKeyboardButton(text="Отмена", callback_data="cancel")
cancel_key = KeyboardButton("Отмена")
cancel_key_button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(cancel_key)

# Кнопки новые поиск

general_menu_inline_btn1 = types.InlineKeyboardButton(text="Поиск", callback_data="general_search")
general_menu_inline_btn2 = types.InlineKeyboardButton(text="Внесение", callback_data="general_insert")
general_menu_inline_btn3 = types.InlineKeyboardButton(text="Справка", callback_data="reference")
general_menu_inline_btn4 = types.InlineKeyboardButton(text="Почта", callback_data="send_files")

general_menu_inline = types.InlineKeyboardMarkup(resize_keyboard=True).row(general_menu_inline_btn1, general_menu_inline_btn2).row(general_menu_inline_btn3, general_menu_inline_btn4)

search_inline_incidents = types.InlineKeyboardButton(text="Эпизоды", callback_data="incidents")
search_inline_criminals = types.InlineKeyboardButton(text="Лица", callback_data="crimes")
search_inline_criminal_case = types.InlineKeyboardButton(text="УД", callback_data="search_case")

search_menu_inline = types.InlineKeyboardMarkup().row(search_inline_incidents, search_inline_criminals, search_inline_criminal_case).add(cancel_button)

inline_reply_incident = types.InlineKeyboardMarkup().row(inline_reply_incident_btn1, inline_reply_incident_btn9).row(inline_reply_incident_btn2, inline_reply_incident_btn3).row(inline_reply_incident_btn4, inline_reply_incident_btn5).add(cancel_button)

inline_reply_crimes_names = types.InlineKeyboardMarkup().row(inline_reply_crimes_btn1, inline_reply_crimes_btn3).add(cancel_button)

# Кнопки справка

inline_reply_reference = types.InlineKeyboardMarkup().row(inline_reply_reference_btn1, inline_reply_reference_btn2).add(cancel_button)

# Кнопки новые поиск

incert_inline_criminals = types.InlineKeyboardButton(text="Лицо", callback_data="add_crimes_name")
incert_inline_case = types.InlineKeyboardButton(text="УД", callback_data="add_case")
incert_inline_inline_incident = types.InlineKeyboardButton(text="Заявку", callback_data="add_new_incident")

incert_menu_inline = types.InlineKeyboardMarkup().row(incert_inline_inline_incident, incert_inline_criminals, incert_inline_case).add(cancel_button)

# Соотнести лицо и ID

insert_id_criminal = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(text="Внести", callback_data="add_id_criminal"), cancel_button)

