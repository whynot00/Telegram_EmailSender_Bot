from aiogram import types
import json


def whitelist_checker(user_id, powers):
    with open("configurations/white_list.json", "r") as file:
        white_list = json.load(file)
        if str(user_id) in str(white_list[powers]):
            return True

