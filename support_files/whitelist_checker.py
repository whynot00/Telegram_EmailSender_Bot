from aiogram import types

def whitelist_checker(user_id):
    with open("configurations/white_list.txt", "r") as file:
        white_list = file.read()
        if str(user_id) not in str(white_list):
            return True