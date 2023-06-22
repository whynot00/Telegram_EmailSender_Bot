# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup

# from misc import dispatcher as dp
# from misc import bot

# import os

# from support_files import parce_update_members_groups as update_members
# from support_files import whitelist_checker as wl_check
# from support_files import send_email
# from support_files import buttons as nav

# class Form_group(StatesGroup):
#     chek_user = State()

# # Доделать надо




# @dp.message_handler(commands="update")
# async def update_members_group(message: types.Message):
#     print("ss")
#     # async with client:
#     #     client.loop.run_until_complete(update_members.main())


#     # if wl_check.whitelist_checker(user_id=message.from_user.id, powers="admin") == True:
#     #     if os.path.exists("logs/member_list.db") == True:
#     #         os.remove("logs/member_list.db")
            




#     # Реакция на выход с отправки /// хз как работает на нескольких этапах????
# @dp.message_handler(text=nav.main_button_2.text, state="*")
# async def poyti_nahooi(message: types.Message, state="*"):
#     await state.finish()
#     await bot.send_message(message.from_user.id, "Выход в галвное меню.", reply_markup=types.ReplyKeyboardRemove())
#     await bot.send_message(message.from_user.id, "Выберите необходимую функцию:", reply_markup=nav.inline_reply_button)


# @dp.callback_query_handler(text="find_group")
# async def start_find(message: types.Message, state=FSMContext):
#     await state.set_state(Form_group.chek_user)
#     await bot.send_message(message.from_user.id, "Отправьте никнейм ID пользователя:", reply_markup=nav.main_button)



    # elif mode == "locate":
    #     cursor.execute(f"SELECT * FROM coordinates")
    #     result_parcing =  cursor.fetchall()

    #     output = []

    #     for index, item in enumerate(result_parcing):
    #         output_info = []
    #         location = item[1], item[2]
    #         if geo(location, data).m < 1000:
    #             cursor.execute(f"SELECT * FROM incidents WHERE incident_id = {item[0]}")
    #             output_info.append(list(cursor.fetchone()))
    #             output_info[0].append(int(geo(location, data).m))
    #             output += output_info\

    #     return output